"""Kata03: How Big? How Fast? - Estimation Calculator

This module implements an estimation calculator for the How Big? How Fast? kata.
It provides tools for rough estimation of bits, storage, and time.

Source: http://codekata.com/kata/kata03-how-big-how-fast/

The kata is about developing intuition for orders of magnitude through
mental estimation. This implementation provides a calculator that can
verify mental estimates and teach estimation techniques.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from math import log2, ceil
from typing import List, Optional, Protocol
from abc import ABC, abstractmethod


# =============================================================================
# Value Objects
# =============================================================================

@dataclass(frozen=True)
class BitEstimate:
    """Estimated bits for unsigned integer representation."""
    value: int
    exact_bits: int
    formula: str
    
    def __str__(self) -> str:
        return f"{self.value:,} ≈ 2^{self.exact_bits} ({self.formula})"


@dataclass(frozen=True)
class StorageEstimate:
    """Estimated storage size."""
    bytes: int
    human_readable: str
    breakdown: str
    
    def __str__(self) -> str:
        return f"{self.human_readable} ({self.bytes:,} bytes) - {self.breakdown}"


@dataclass(frozen=True)
class TimeEstimate:
    """Estimated time duration."""
    milliseconds: float
    human_readable: str
    formula: str
    
    def __str__(self) -> str:
        return f"{self.human_readable} ({self.formula})"


# =============================================================================
# Enums
# =============================================================================

class EstimationCategory(Enum):
    BITS = "bits"
    STORAGE = "storage"
    TIME = "time"


# =============================================================================
# Repository Interface
# =============================================================================

class EstimationRepository(Protocol):
    """Repository for caching estimation results."""
    
    def save(self, category: EstimationCategory, input_value: str, result: object) -> None: ...
    
    def get_history(self, category: Optional[EstimationCategory] = None) -> List[object]: ...
    
    def clear(self) -> None: ...


class InMemoryEstimationRepository:
    """In-memory estimation repository."""
    
    def __init__(self):
        self._history: List[tuple] = []  # (category, input, result)
    
    def save(self, category: EstimationCategory, input_value: str, result: object) -> None:
        self._history.append((category, input_value, result))
    
    def get_history(self, category: Optional[EstimationCategory] = None) -> List[object]:
        if category:
            return [r for c, i, r in self._history if c == category]
        return [r for c, i, r in self._history]
    
    def clear(self) -> None:
        self._history.clear()


# =============================================================================
# Domain Services
# =============================================================================

class BitEstimationService:
    """Service for bit-level estimations."""
    
    @staticmethod
    def bits_for_unsigned(n: int) -> BitEstimate:
        """Calculate bits needed for unsigned representation of n."""
        if n <= 0:
            return BitEstimate(0, 0, "N/A (n ≤ 0)")
        
        # Exact: ceil(log2(n + 1))
        exact = ceil(log2(n + 1))
        # Approximation: log10(n) * log2(10) ≈ log10(n) * 3.322
        approx = log2(n)
        
        formula = f"ceil(log2({n:,} + 1)) = {exact}"
        
        return BitEstimate(n, exact, formula)
    
    @staticmethod
    def bits_for_range(max_value: int) -> BitEstimate:
        """Bits needed to represent range 0..max_value."""
        if max_value < 0:
            return BitEstimate(0, 0, "N/A")
        exact = ceil(log2(max_value + 1))
        return BitEstimate(max_value, exact, f"Range 0..{max_value:,} → ceil(log2({max_value:,}+1)) = {exact}")


class StorageEstimationService:
    """Service for storage estimations."""
    
    # Constants
    CHARS_PER_NAME = 30
    CHARS_PER_ADDRESS = 50
    CHARS_PER_PHONE = 15
    CHARS_PER_RECORD = CHARS_PER_NAME + CHARS_PER_ADDRESS + CHARS_PER_PHONE  # 95
    
    POINTER_SIZE_32BIT = 4  # bytes
    POINTER_SIZE_64BIT = 8  # bytes
    INT_SIZE_32BIT = 4  # bytes
    NODE_OVERHEAD_32BIT = 16  # 3 pointers + color/balance + padding
    NODE_OVERHEAD_64BIT = 28  # 3 pointers + color/balance + padding (aligned)
    
    @classmethod
    def estimate_town_records(cls, num_residences: int, 
                               chars_per_name: int = CHARS_PER_NAME,
                               chars_per_address: int = CHARS_PER_ADDRESS,
                               chars_per_phone: int = CHARS_PER_PHONE) -> StorageEstimate:
        """Estimate storage for town records."""
        chars_per_record = chars_per_name + chars_per_address + chars_per_phone
        total_chars = num_residences * chars_per_record
        bytes_needed = total_chars  # 1 byte per char (ASCII)
        
        # Human readable
        if bytes_needed >= 1_000_000_000:
            hr = f"{bytes_needed / 1_000_000_000:.1f} GB"
        elif bytes_needed >= 1_000_000:
            hr = f"{bytes_needed / 1_000_000:.1f} MB"
        elif bytes_needed >= 1_000:
            hr = f"{bytes_needed / 1_000:.1f} KB"
        else:
            hr = f"{bytes_needed} B"
        
        breakdown = (f"{num_residences:,} residences × "
                    f"({chars_per_name}+{chars_per_address}+{chars_per_phone}) chars = "
                    f"{total_chars:,} chars ≈ {hr}")
        
        return StorageEstimate(bytes_needed, hr, breakdown)
    
    @classmethod
    def estimate_binary_tree_storage(cls, num_nodes: int, 
                                      is_64bit: bool = False) -> StorageEstimate:
        """Estimate storage for binary tree with given number of nodes."""
        pointer_size = cls.POINTER_SIZE_64BIT if is_64bit else cls.POINTER_SIZE_32BIT
        int_size = cls.INT_SIZE_32BIT
        overhead = cls.NODE_OVERHEAD_64BIT if is_64bit else cls.NODE_OVERHEAD_32BIT
        
        # Per node: value (int) + left ptr + right ptr + parent ptr + color/balance
        # 32-bit: 4 (int) + 3*4 (pointers) + 8 (overhead) = 28
        # 64-bit: 4 (int) + 3*8 (pointers) + 24 (overhead) = 52
        bytes_per_node = int_size + (3 * pointer_size) + overhead
        total_bytes = num_nodes * bytes_per_node
        
        # Levels ≈ log2(n)
        levels = ceil(log2(num_nodes + 1))
        
        arch = "64-bit" if is_64bit else "32-bit"
        if total_bytes >= 1_000_000_000:
            hr = f"{total_bytes / 1_000_000_000:.1f} GB"
        elif total_bytes >= 1_000_000:
            hr = f"{total_bytes / 1_000_000:.1f} MB"
        elif total_bytes >= 1_000:
            hr = f"{total_bytes / 1_000:.1f} KB"
        else:
            hr = f"{total_bytes} B"
        
        breakdown = (f"{num_nodes:,} nodes × {bytes_per_node} bytes/node ({arch}) "
                    f"= {total_bytes:,} bytes ≈ {hr}, ~{levels} levels")
        
        return StorageEstimate(total_bytes, hr, breakdown)


class TimeEstimationService:
    """Service for time estimations."""
    
    # Constants
    BAUD_56K = 56_000  # bits per second
    BYTES_PER_PAGE = 2_000  # rough estimate: ~2000 chars per page
    BITS_PER_BYTE = 8
    
    @classmethod
    def estimate_modem_transfer(cls, pages: int, baud: int = BAUD_56K) -> TimeEstimate:
        """Estimate time to transfer text over modem."""
        total_chars = pages * cls.BYTES_PER_PAGE
        total_bits = total_chars * cls.BITS_PER_BYTE
        seconds = total_bits / baud
        ms = seconds * 1000
        
        if seconds >= 3600:
            hr = f"{seconds / 3600:.1f} hours"
        elif seconds >= 60:
            hr = f"{seconds / 60:.1f} minutes"
        else:
            hr = f"{seconds:.1f} seconds"
        
        formula = f"{pages} pages × {cls.BYTES_PER_PAGE} chars × 8 bits / {baud:,} bps = {seconds:.1f}s"
        
        return TimeEstimate(ms, hr, formula)
    
    @classmethod
    def estimate_binary_search_scaling(cls, time_10k: float, time_100k: float, 
                                        target_n: int) -> TimeEstimate:
        """Estimate binary search time for target_n based on known measurements.
        
        Binary search is O(log n). If T(n) = k * log2(n), we can solve for k.
        """
        # Using the two known points to estimate k
        # T(10000) = k * log2(10000) ≈ k * 13.29
        # T(100000) = k * log2(100000) ≈ k * 16.61
        
        log_10k = log2(10_000)
        log_100k = log2(100_000)
        log_target = log2(target_n)
        
        # Average k from both points
        k1 = time_10k / log_10k
        k2 = time_100k / log_100k
        k = (k1 + k2) / 2
        
        estimated_time = k * log_target
        
        formula = (f"T(n) = k * log2(n); k ≈ ({time_10k}/{log_10k:.2f} + "
                  f"{time_100k}/{log_100k:.2f})/2 = {k:.3f}; "
                  f"T({target_n:,}) = {k:.3f} * {log_target:.2f} = {estimated_time:.2f}ms")
        
        if estimated_time >= 1000:
            hr = f"{estimated_time / 1000:.2f} seconds"
        else:
            hr = f"{estimated_time:.1f} ms"
        
        return TimeEstimate(estimated_time, hr, formula)
    
    @classmethod
    def estimate_password_cracking(cls, max_length: int, charset_size: int, 
                                    hash_time_ms: float) -> TimeEstimate:
        """Estimate time to brute-force password space."""
        # Total combinations = charset_size^1 + charset_size^2 + ... + charset_size^max_length
        # ≈ charset_size^max_length for large max_length
        total_combinations = sum(charset_size ** i for i in range(1, max_length + 1))
        
        total_time_ms = total_combinations * hash_time_ms
        total_time_years = total_time_ms / (1000 * 60 * 60 * 24 * 365.25)
        
        if total_time_years >= 1:
            hr = f"{total_time_years:.2e} years"
        elif total_time_ms >= 1000 * 60 * 60 * 24:
            hr = f"{total_time_ms / (1000 * 60 * 60 * 24):.1f} days"
        elif total_time_ms >= 1000 * 60 * 60:
            hr = f"{total_time_ms / (1000 * 60 * 60):.1f} hours"
        else:
            hr = f"{total_time_ms / 1000:.1f} seconds"
        
        formula = (f"Σ({charset_size}^i) for i=1..{max_length} = {total_combinations:.2e} "
                  f"combinations × {hash_time_ms}ms = {total_time_ms:.2e}ms")
        
        return TimeEstimate(total_time_ms, hr, formula)


# =============================================================================
# Commands (CQRS)
# =============================================================================

@dataclass
class EstimateBitsCommand:
    value: int


@dataclass
class EstimateStorageCommand:
    category: str  # "town_records" or "binary_tree"
    num_items: int
    is_64bit: bool = False
    chars_per_name: int = 30
    chars_per_address: int = 50
    chars_per_phone: int = 15


@dataclass
class EstimateTimeCommand:
    category: str  # "modem", "binary_search", "password"
    pages: int = 0
    baud: int = 56_000
    time_10k: float = 0.0
    time_100k: float = 0.0
    target_n: int = 0
    max_length: int = 0
    charset_size: int = 0
    hash_time_ms: float = 0.0


class EstimationCommandHandler:
    """Command handler for estimation operations."""
    
    def __init__(self, repository: EstimationRepository):
        self._repository = repository
        self._bit_service = BitEstimationService()
        self._storage_service = StorageEstimationService()
        self._time_service = TimeEstimationService()
    
    def handle_estimate_bits(self, cmd: EstimateBitsCommand) -> BitEstimate:
        result = self._bit_service.bits_for_unsigned(cmd.value)
        self._repository.save(EstimationCategory.BITS, str(cmd.value), result)
        return result
    
    def handle_estimate_storage(self, cmd: EstimateStorageCommand):
        if cmd.category == "town_records":
            result = self._storage_service.estimate_town_records(
                cmd.num_items,
                chars_per_name=cmd.chars_per_name,
                chars_per_address=cmd.chars_per_address,
                chars_per_phone=cmd.chars_per_phone
            )
        elif cmd.category == "binary_tree":
            result = self._storage_service.estimate_binary_tree_storage(cmd.num_items, cmd.is_64bit)
        else:
            raise ValueError(f"Unknown storage category: {cmd.category}")
        self._repository.save(EstimationCategory.STORAGE, str(cmd.num_items), result)
        return result
    
    def handle_estimate_time(self, cmd: EstimateTimeCommand):
        if cmd.category == "modem":
            result = self._time_service.estimate_modem_transfer(cmd.pages, cmd.baud)
        elif cmd.category == "binary_search":
            result = self._time_service.estimate_binary_search_scaling(cmd.time_10k, cmd.time_100k, cmd.target_n)
        elif cmd.category == "password":
            result = self._time_service.estimate_password_cracking(cmd.max_length, cmd.charset_size, cmd.hash_time_ms)
        else:
            raise ValueError(f"Unknown time category: {cmd.category}")
        self._repository.save(EstimationCategory.TIME, str(cmd.category), result)
        return result


# =============================================================================
# Queries (CQRS)
# =============================================================================

@dataclass
class EstimationQuery:
    category: Optional[EstimationCategory] = None


class EstimationQueryHandler:
    """Query handler for estimation history."""
    
    def __init__(self, repository: EstimationRepository):
        self._repository = repository
    
    def handle_query(self, query: EstimationQuery) -> List[object]:
        return self._repository.get_history(query.category)


# =============================================================================
# Facade
# =============================================================================

class HowBigHowFast:
    """Main facade for How Big? How Fast? estimation calculator."""
    
    def __init__(self):
        self._repository = InMemoryEstimationRepository()
        self._command_handler = EstimationCommandHandler(self._repository)
        self._query_handler = EstimationQueryHandler(self._repository)
    
    # Bit estimations
    def estimate_bits(self, n: int) -> BitEstimate:
        cmd = EstimateBitsCommand(value=n)
        return self._command_handler.handle_estimate_bits(cmd)
    
    def estimate_bits_range(self, max_value: int) -> BitEstimate:
        return BitEstimationService.bits_for_range(max_value)
    
    # Storage estimations
    def estimate_town_records(self, num_residences: int, 
                               chars_per_name: int = 30,
                               chars_per_address: int = 50,
                               chars_per_phone: int = 15) -> StorageEstimate:
        cmd = EstimateStorageCommand(
            category="town_records",
            num_items=num_residences,
            chars_per_name=chars_per_name,
            chars_per_address=chars_per_address,
            chars_per_phone=chars_per_phone
        )
        return self._command_handler.handle_estimate_storage(cmd)
    
    def estimate_binary_tree(self, num_nodes: int, is_64bit: bool = False) -> StorageEstimate:
        cmd = EstimateStorageCommand(
            category="binary_tree",
            num_items=num_nodes,
            is_64bit=is_64bit
        )
        return self._command_handler.handle_estimate_storage(cmd)
    
    # Time estimations
    def estimate_modem_transfer(self, pages: int, baud: int = 56_000) -> TimeEstimate:
        cmd = EstimateTimeCommand(
            category="modem",
            pages=pages,
            baud=baud
        )
        return self._command_handler.handle_estimate_time(cmd)
    
    def estimate_binary_search_time(self, time_10k: float, time_100k: float, 
                                     target_n: int) -> TimeEstimate:
        cmd = EstimateTimeCommand(
            category="binary_search",
            time_10k=time_10k,
            time_100k=time_100k,
            target_n=target_n
        )
        return self._command_handler.handle_estimate_time(cmd)
    
    def estimate_password_cracking(self, max_length: int, charset_size: int, 
                                    hash_time_ms: float) -> TimeEstimate:
        cmd = EstimateTimeCommand(
            category="password",
            max_length=max_length,
            charset_size=charset_size,
            hash_time_ms=hash_time_ms
        )
        return self._command_handler.handle_estimate_time(cmd)
    
    # History
    def get_history(self, category: Optional[EstimationCategory] = None) -> List[object]:
        query = EstimationQuery(category=category)
        return self._query_handler.handle_query(query)
    
    def clear_history(self):
        self._repository.clear()


# =============================================================================
# Functional Alternative
# =============================================================================

def estimate_bits(n: int) -> int:
    """Functional interface: estimate bits for unsigned n."""
    if n <= 0:
        return 0
    return ceil(log2(n + 1))


def estimate_bits_ceil_log2(n: int) -> int:
    """Alternative: ceil(log2(n)) for n > 0."""
    if n <= 0:
        return 0
    return ceil(log2(n))


def estimate_bits_range(max_value: int) -> int:
    if max_value < 0:
        return 0
    return ceil(log2(max_value + 1))


def estimate_town_records_storage(num_residences: int) -> int:
    """Return bytes needed for town records."""
    return num_residences * 95  # 95 chars per record


def estimate_binary_tree_storage(num_nodes: int, is_64bit: bool = False) -> int:
    """Return bytes needed for binary tree storage."""
    if is_64bit:
        # 64-bit: 4 (int) + 3*8 (pointers) + 24 (overhead) = 52
        bytes_per_node = 4 + (3 * 8) + 24
    else:
        # 32-bit: 4 (int) + 3*4 (pointers) + 16 (overhead) = 32
        bytes_per_node = 4 + (3 * 4) + 16
    return num_nodes * bytes_per_node


def estimate_modem_transfer_time(pages: int, baud: int = 56000) -> float:
    """Return time in seconds."""
    total_bits = pages * 2000 * 8
    return total_bits / baud


def estimate_binary_search_time(time_10k: float, time_100k: float, target_n: int) -> float:
    log_10k = log2(10_000)
    log_100k = log2(100_000)
    log_target = log2(target_n)
    k1 = time_10k / log_10k
    k2 = time_100k / log_100k
    k = (k1 + k2) / 2
    return k * log_target


def estimate_password_cracking_time(max_length: int, charset_size: int, hash_time_ms: float) -> float:
    total = sum(charset_size ** i for i in range(1, max_length + 1))
    return total * hash_time_ms


# =============================================================================
# Kata Answers (from the kata questions)
# =============================================================================

def get_kata_answers() -> dict:
    """Return the answers to all kata questions."""
    calculator = HowBigHowFast()
    
    answers = {}
    
    # How Big? - Bits
    answers["bits"] = {}
    for n in [1_000, 1_000_000, 1_000_000_000, 1_000_000_000_000, 8_000_000_000_000]:
        result = calculator.estimate_bits(n)
        answers["bits"][n] = f"~{result.exact_bits} bits"
    
    # How Big? - Town records
    answers["town_records"] = str(calculator.estimate_town_records(20_000))
    
    # How Big? - Binary tree
    answers["binary_tree_32bit"] = str(calculator.estimate_binary_tree(1_000_000, is_64bit=False))
    answers["binary_tree_64bit"] = str(calculator.estimate_binary_tree(1_000_000, is_64bit=True))
    
    # How Fast? - Modem
    answers["modem_transfer"] = str(calculator.estimate_modem_transfer(1_200))
    
    # How Fast? - Binary search
    answers["binary_search_10m"] = str(calculator.estimate_binary_search_time(4.5, 6.0, 10_000_000))
    
    # How Fast? - Password cracking
    answers["password_cracking"] = str(calculator.estimate_password_cracking(16, 96, 1.0))
    
    return answers


if __name__ == "__main__":
    print("=== Kata03: How Big? How Fast? - Answers ===\n")
    
    calc = HowBigHowFast()
    answers = get_kata_answers()
    
    print("=== How Big? ===")
    print("\n1. Bits for unsigned representation:")
    for n, bits in answers["bits"].items():
        print(f"   {n:>15,} → {bits}")
    
    print(f"\n2. Town records (20,000 residences):")
    print(f"   {answers['town_records']}")
    
    print(f"\n3. Binary tree (1M integers):")
    print(f"   32-bit: {answers['binary_tree_32bit']}")
    print(f"   64-bit: {answers['binary_tree_64bit']}")
    
    print("\n=== How Fast? ===")
    print(f"\n4. Modem transfer (1,200 pages @ 56k baud):")
    print(f"   {answers['modem_transfer']}")
    
    print(f"\n5. Binary search (10M elements):")
    print(f"   {answers['binary_search_10m']}")
    
    print(f"\n6. Password cracking (16 chars, 96 charset, 1ms/hash):")
    print(f"   {answers['password_cracking']}")