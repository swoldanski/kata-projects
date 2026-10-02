"""Kata05: Bloom Filters - Probabilistic Data Structure

This module implements a Bloom filter from scratch, a space-efficient
probabilistic data structure for set membership testing.

Source: http://codekata.com/kata/kata05-bloom-filters/

Key Properties:
- False positives possible, false negatives impossible
- Space-efficient: O(m) bits for m-bit array
- k hash functions for k-bit positions per element
- False positive rate: (1 - e^(-kn/m))^k

Source: http://codekata.com/kata/kata05-bloom-filters/
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Set, Iterator, Protocol
from abc import ABC, abstractmethod
import hashlib
import math
import random


# =============================================================================
# Value Objects
# =============================================================================

@dataclass(frozen=True)
class BloomFilterConfig:
    """Immutable configuration for Bloom filter."""
    expected_elements: int          # n: expected number of elements
    false_positive_rate: float      # p: desired false positive probability
    
    def __post_init__(self):
        if self.expected_elements <= 0:
            raise ValueError("expected_elements must be positive")
        if not 0 < self.false_positive_rate < 1:
            raise ValueError("false_positive_rate must be between 0 and 1")
    
    @property
    def optimal_bit_array_size(self) -> int:
        """Calculate optimal bit array size m = -n * ln(p) / (ln(2)^2)."""
        m = -self.expected_elements * math.log(self.false_positive_rate) / (math.log(2) ** 2)
        return max(1, int(math.ceil(m)))
    
    @property
    def optimal_hash_count(self) -> int:
        """Calculate optimal number of hash functions k = (m/n) * ln(2)."""
        m = self.optimal_bit_array_size
        k = (m / self.expected_elements) * math.log(2)
        return max(1, int(round(k)))


@dataclass
class BloomFilterStats:
    """Statistics for Bloom filter performance tracking."""
    elements_added: int = 0
    queries_made: int = 0
    false_positives_detected: int = 0
    
    @property
    def empirical_false_positive_rate(self) -> float:
        if self.queries_made == 0:
            return 0.0
        return self.false_positives_detected / self.queries_made


# =============================================================================
# Hash Function Strategies
# =============================================================================

class HashFunction(ABC):
    """Abstract base for hash functions."""
    
    @abstractmethod
    def hash(self, item: str, seed: int, modulus: int) -> int:
        """Hash item with given seed, return index in [0, modulus)."""
        pass


class MD5HashFunction(HashFunction):
    """MD5-based hash function with seed."""
    
    def hash(self, item: str, seed: int, modulus: int) -> int:
        data = f"{seed}:{item}".encode('utf-8')
        return int(hashlib.md5(data).hexdigest(), 16) % modulus


class SHA256HashFunction(HashFunction):
    """SHA256-based hash function with seed."""
    
    def hash(self, item: str, seed: int, modulus: int) -> int:
        data = f"{seed}:{item}".encode('utf-8')
        return int(hashlib.sha256(data).hexdigest(), 16) % modulus


class FNVHashFunction(HashFunction):
    """FNV-1a hash function with seed."""
    
    FNV_OFFSET_BASIS = 0x811c9dc5
    FNV_PRIME = 0x01000193
    
    def hash(self, item: str, seed: int, modulus: int) -> int:
        hash_val = self.FNV_OFFSET_BASIS ^ seed
        for byte in item.encode('utf-8'):
            hash_val ^= byte
            hash_val = (hash_val * self.FNV_PRIME) & 0xFFFFFFFF
        return hash_val % modulus


class DoubleHashFunction(HashFunction):
    """Double hashing for k hash functions from 2 base hashes.
    
    h_i(x) = (h1(x) + i * h2(x)) % m
    This is more efficient than computing k independent hashes.
    """
    
    def __init__(self, hash1: HashFunction = None, hash2: HashFunction = None):
        self.hash1 = hash1 or MD5HashFunction()
        self.hash2 = hash2 or SHA256HashFunction()
    
    def hash(self, item: str, seed: int, modulus: int) -> int:
        # Not used directly; use hash_k instead
        raise NotImplementedError("Use hash_k for double hashing")
    
    def hash_k(self, item: str, k: int, modulus: int) -> List[int]:
        """Generate k hash values using double hashing."""
        h1 = self.hash1.hash(item, 0, modulus)
        h2 = self.hash2.hash(item, 1, modulus)
        if h2 == 0:
            h2 = 1  # Ensure h2 != 0
        return [(h1 + i * h2) % modulus for i in range(k)]


# =============================================================================
# Repository Interface
# =============================================================================

class BloomFilterRepository(Protocol):
    """Repository for persisting Bloom filter state."""
    
    def save(self, bloom_filter: 'BloomFilter') -> None: ...
    
    def load(self, filter_id: str) -> Optional['BloomFilter']: ...
    
    def delete(self, filter_id: str) -> None: ...


class InMemoryBloomFilterRepository:
    """In-memory repository for Bloom filters."""
    
    def __init__(self):
        self._filters: dict = {}
    
    def save(self, bloom_filter: 'BloomFilter') -> None:
        self._filters[bloom_filter.filter_id] = bloom_filter
    
    def load(self, filter_id: str) -> Optional['BloomFilter']:
        return self._filters.get(filter_id)
    
    def delete(self, filter_id: str) -> None:
        self._filters.pop(filter_id, None)


# =============================================================================
# Domain Entity: Bloom Filter
# =============================================================================

@dataclass
class BloomFilter:
    """Bloom filter implementation with configurable parameters."""
    
    filter_id: str
    bit_array: bytearray
    config: BloomFilterConfig
    hash_function: HashFunction = field(default_factory=DoubleHashFunction)
    stats: BloomFilterStats = field(default_factory=BloomFilterStats)
    
    def __post_init__(self):
        if len(self.bit_array) != self.config.optimal_bit_array_size:
            raise ValueError("Bit array size must match config optimal size")
    
    @classmethod
    def create(cls, filter_id: str, config: BloomFilterConfig, 
               hash_function: HashFunction = None) -> 'BloomFilter':
        """Factory method to create a new Bloom filter."""
        m = config.optimal_bit_array_size
        bit_array = bytearray(m)
        return cls(
            filter_id=filter_id,
            bit_array=bit_array,
            config=config,
            hash_function=hash_function or DoubleHashFunction()
        )
    
    def _get_indices(self, item: str) -> List[int]:
        """Get k bit indices for an item using double hashing."""
        if isinstance(self.hash_function, DoubleHashFunction):
            return self.hash_function.hash_k(item, self.config.optimal_hash_count, len(self.bit_array))
        else:
            # Fallback: use seed-based hashing
            k = self.config.optimal_hash_count
            m = len(self.bit_array)
            return [self.hash_function.hash(item, i, m) for i in range(k)]
    
    def add(self, item: str) -> None:
        """Add item to the Bloom filter."""
        indices = self._get_indices(item)
        for idx in indices:
            byte_idx = idx // 8
            bit_idx = idx % 8
            self.bit_array[byte_idx] |= (1 << bit_idx)
        self.stats.elements_added += 1
    
    def __contains__(self, item: str) -> bool:
        """Check if item might be in the set."""
        indices = self._get_indices(item)
        for idx in indices:
            byte_idx = idx // 8
            bit_idx = idx % 8
            if not (self.bit_array[byte_idx] & (1 << bit_idx)):
                self.stats.queries_made += 1
                return False
        self.stats.queries_made += 1
        return True
    
    def might_contain(self, item: str) -> bool:
        """Explicit check if item might be in set."""
        return item in self
    
    def is_empty(self) -> bool:
        """Check if filter is empty (no bits set)."""
        return all(b == 0 for b in self.bit_array)
    
    def fill_ratio(self) -> float:
        """Return fraction of bits set to 1."""
        total_bits = len(self.bit_array) * 8
        set_bits = sum(bin(b).count('1') for b in self.bit_array)
        return set_bits / total_bits if total_bits > 0 else 0.0
    
    def estimated_false_positive_rate(self) -> float:
        """Calculate theoretical false positive rate."""
        k = self.config.optimal_hash_count
        m = len(self.bit_array) * 8
        n = self.stats.elements_added
        if n == 0:
            return 0.0
        return (1 - math.exp(-k * n / m)) ** k


# =============================================================================
# Domain Services
# =============================================================================

class BloomFilterService:
    """Domain service for Bloom filter operations."""
    
    def __init__(self, repository: BloomFilterRepository):
        self._repository = repository
    
    def create_filter(self, filter_id: str, expected_elements: int,
                      false_positive_rate: float,
                      hash_function: HashFunction = None) -> BloomFilter:
        """Create and save a new Bloom filter with optimal parameters."""
        config = BloomFilterConfig(expected_elements, false_positive_rate)
        bf = BloomFilter.create(filter_id, config, hash_function)
        self._repository.save(bf)
        return bf
    
    def add_to_filter(self, filter_id: str, item: str) -> bool:
        """Add item to filter. Returns True if successful."""
        bf = self._repository.load(filter_id)
        if not bf:
            return False
        bf.add(item)
        self._repository.save(bf)
        return True
    
    def check_filter(self, filter_id: str, item: str) -> Optional[bool]:
        """Check if item might be in filter. Returns None if filter not found."""
        bf = self._repository.load(filter_id)
        if not bf:
            return None
        return item in bf
    
    def get_stats(self, filter_id: str) -> Optional[BloomFilterStats]:
        """Get filter statistics."""
        bf = self._repository.load(filter_id)
        return bf.stats if bf else None


# =============================================================================
# Commands (CQRS)
# =============================================================================

@dataclass
class CreateBloomFilterCommand:
    filter_id: str
    expected_elements: int
    false_positive_rate: float


@dataclass
class AddToBloomFilterCommand:
    filter_id: str
    item: str


@dataclass
class QueryBloomFilterCommand:
    filter_id: str
    item: str


class BloomFilterCommandHandler:
    """Command handler for Bloom filter operations."""
    
    def __init__(self, service: BloomFilterService):
        self._service = service
    
    def handle_create(self, cmd: CreateBloomFilterCommand) -> BloomFilter:
        return self._service.create_filter(
            cmd.filter_id, cmd.expected_elements, cmd.false_positive_rate
        )
    
    def handle_add(self, cmd: AddToBloomFilterCommand) -> bool:
        return self._service.add_to_filter(cmd.filter_id, cmd.item)
    
    def handle_query(self, cmd: QueryBloomFilterCommand) -> Optional[bool]:
        return self._service.check_filter(cmd.filter_id, cmd.item)


# =============================================================================
# Queries (CQRS)
# =============================================================================

@dataclass
class BloomFilterQuery:
    filter_id: str


@dataclass
class BloomFilterQueryResult:
    exists: Optional[bool]
    stats: Optional[BloomFilterStats]
    estimated_fpr: float


class BloomFilterQueryHandler:
    """Query handler for Bloom filter operations."""
    
    def __init__(self, service: BloomFilterService):
        self._service = service
    
    def handle_query(self, query: BloomFilterQuery) -> BloomFilterQueryResult:
        bf = self._service._repository.load(query.filter_id)
        if not bf:
            return BloomFilterQueryResult(None, None, 0.0)
        return BloomFilterQueryResult(
            exists=None,  # Not a query for specific item
            stats=bf.stats,
            estimated_fpr=bf.estimated_false_positive_rate()
        )


# =============================================================================
# Facade
# =============================================================================

class BloomFilters:
    """Main facade for Bloom filter operations."""
    
    def __init__(self):
        self._repository = InMemoryBloomFilterRepository()
        self._service = BloomFilterService(self._repository)
        self._command_handler = BloomFilterCommandHandler(self._service)
        self._query_handler = BloomFilterQueryHandler(self._service)
    
    # Commands
    def create_filter(self, filter_id: str, expected_elements: int, 
                       false_positive_rate: float) -> BloomFilter:
        config = BloomFilterConfig(expected_elements, false_positive_rate)
        cmd = CreateBloomFilterCommand(
            filter_id=filter_id,
            expected_elements=expected_elements,
            false_positive_rate=false_positive_rate
        )
        return self._command_handler.handle_create(cmd)
    
    def add(self, filter_id: str, item: str) -> bool:
        cmd = AddToBloomFilterCommand(filter_id=filter_id, item=item)
        return self._command_handler.handle_add(cmd)
    
    # Queries
    def check(self, filter_id: str, item: str) -> Optional[bool]:
        cmd = QueryBloomFilterCommand(filter_id=filter_id, item=item)
        return self._command_handler.handle_query(cmd)
    
    def get_stats(self, filter_id: str) -> Optional[BloomFilterStats]:
        return self._service.get_stats(filter_id)
    
    def get_estimated_fpr(self, filter_id: str) -> float:
        bf = self._repository.load(filter_id)
        return bf.estimated_false_positive_rate() if bf else 0.0
    
    def get_fill_ratio(self, filter_id: str) -> float:
        bf = self._repository.load(filter_id)
        return bf.fill_ratio() if bf else 0.0


# =============================================================================
# Functional Alternative
# =============================================================================

class BloomFilterFunctional:
    """Functional-style Bloom filter implementation."""
    
    def __init__(self, m: int, k: int, hash_func: Callable = None):
        self.m = m
        self.k = k
        self.bit_array = bytearray(m)
        self.hash_func = hash_func or self._default_hash
    
    def _default_hash(self, item: str, seed: int, m: int) -> int:
        return int(hashlib.md5(f"{seed}:{item}".encode()).hexdigest(), 16) % m
    
    def add(self, item: str) -> None:
        for i in range(self.k):
            idx = self.hash_func(item, i, self.m)
            self.bit_array[idx // 8] |= (1 << (idx % 8))
    
    def __contains__(self, item: str) -> bool:
        for i in range(self.k):
            idx = self.hash_func(item, i, self.m)
            if not (self.bit_array[idx // 8] & (1 << (idx % 8))):
                return False
        return True
    
    def add_multiple(self, items: Iterator[str]) -> None:
        for item in items:
            self.add(item)
    
    def check_multiple(self, items: List[str]) -> List[bool]:
        return [item in self for item in items]


def create_bloom_filter(expected_elements: int, false_positive_rate: float) -> BloomFilterFunctional:
    """Factory function to create functional Bloom filter with optimal parameters."""
    config = BloomFilterConfig(expected_elements, false_positive_rate)
    return BloomFilterFunctional(config.optimal_bit_array_size, config.optimal_hash_count)


# =============================================================================
# Example Usage & Demo
# =============================================================================

if __name__ == "__main__":
    print("=== Kata05: Bloom Filters - Demo ===\n")
    
    # Create Bloom filter with optimal parameters
    bf = BloomFilters()
    bf.create_filter("spell_checker", expected_elements=10000, false_positive_rate=0.01)
    
    # Add dictionary words
    dictionary = ["hello", "world", "python", "bloom", "filter", "test", "data"]
    for word in dictionary:
        bf.add("spell_checker", word)
    
    # Test queries
    test_words = ["hello", "world", "goodbye", "python", "unknown"]
    print("Spell checker demo:")
    for word in test_words:
        result = bf.check("spell_checker", word)
        print(f"  '{word}': {result}")
    
    # Stats
    stats = bf.get_stats("spell_checker")
    print(f"\nStats: {stats.elements_added} added, {stats.queries_made} queries")
    print(f"Estimated FPR: {bf.get_estimated_fpr('spell_checker'):.4f}")
    print(f"Fill ratio: {bf.get_fill_ratio('spell_checker'):.4f}")
    
    # Functional usage
    print("\nFunctional usage:")
    bf_func = create_bloom_filter(1000, 0.01)
    bf_func.add_multiple(["apple", "banana", "cherry"])
    print(f"'apple' in filter: {'apple' in bf_func}")
    print(f"'orange' in filter: {'orange' in bf_func}")
    
    # False positive rate estimation
    print("\nFalse positive rate analysis:")
    print(f"Optimal m (1000 elements, 1% FPR): {BloomFilterConfig(1000, 0.01).optimal_bit_array_size} bits")
    print(f"Optimal k: {BloomFilterConfig(1000, 0.01).optimal_hash_count}")