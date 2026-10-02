"""Tests for Kata05: Bloom Filters - Probabilistic Data Structure."""

import pytest
from math import log2
from kata05_bloom_filters import (
    BloomFilters,
    BloomFilter,
    BloomFilterConfig,
    BloomFilterStats,
    InMemoryBloomFilterRepository,
    BloomFilterFunctional,
    create_bloom_filter,
    DoubleHashFunction,
    MD5HashFunction,
    SHA256HashFunction,
    FNVHashFunction,
    BloomFilterService,
)


class TestBloomFilters:
    """Test cases for Kata05: Bloom Filters."""

    def setup_method(self):
        """Create a fresh BloomFilters instance for each test."""
        self.bf_system = BloomFilters()

    # =========================================================================
    # Configuration Tests
    # =========================================================================

    def test_config_optimal_bit_array_size(self):
        """Test optimal bit array size calculation."""
        # n=1000, p=0.01 -> m ≈ 9585-9586 bits (floating point precision)
        config = BloomFilterConfig(1000, 0.01)
        assert config.optimal_bit_array_size in (9585, 9586)
        
        # n=10000, p=0.001 -> m ≈ 143776 bits
        config = BloomFilterConfig(10000, 0.001)
        assert config.optimal_bit_array_size in (143775, 143776, 143777)

    def test_config_optimal_hash_count(self):
        """Test optimal hash count calculation."""
        config = BloomFilterConfig(1000, 0.01)
        assert config.optimal_hash_count == 7  # (9585/1000) * ln(2) ≈ 6.64 -> 7

    def test_config_validation(self):
        """Test config validation."""
        with pytest.raises(ValueError):
            BloomFilterConfig(0, 0.01)
        with pytest.raises(ValueError):
            BloomFilterConfig(1000, 0)
        with pytest.raises(ValueError):
            BloomFilterConfig(1000, 1.0)
        with pytest.raises(ValueError):
            BloomFilterConfig(1000, -0.01)

    # =========================================================================
    # Hash Function Tests
    # =========================================================================

    def test_md5_hash_function(self):
        """MD5 hash function should produce consistent results."""
        hf = MD5HashFunction()
        idx1 = hf.hash("hello", 0, 1000)
        idx2 = hf.hash("hello", 0, 1000)
        assert idx1 == idx2
        assert 0 <= idx1 < 1000
        
        # Different seeds should give different results
        idx3 = hf.hash("hello", 1, 1000)
        assert idx1 != idx3 or idx1 == 0  # Could theoretically be same

    def test_sha256_hash_function(self):
        """SHA256 hash function."""
        hf = SHA256HashFunction()
        idx1 = hf.hash("hello", 0, 1000)
        idx2 = hf.hash("hello", 0, 1000)
        assert idx1 == idx2

    def test_fnv_hash_function(self):
        """FNV hash function."""
        hf = FNVHashFunction()
        idx1 = hf.hash("hello", 0, 1000)
        idx2 = hf.hash("hello", 0, 1000)
        assert idx1 == idx2

    def test_double_hash_function(self):
        """Double hashing should produce k distinct indices."""
        dh = DoubleHashFunction()
        indices = dh.hash_k("hello", 5, 1000)
        assert len(indices) == 5
        assert len(set(indices)) == 5  # All distinct
        assert all(0 <= idx < 1000 for idx in indices)

    def test_double_hash_deterministic(self):
        """Double hashing should be deterministic."""
        dh = DoubleHashFunction()
        indices1 = dh.hash_k("hello", 5, 1000)
        indices2 = dh.hash_k("hello", 5, 1000)
        assert indices1 == indices2

    # =========================================================================
    # Bloom Filter Configuration Tests
    # =========================================================================

    def test_bloom_filter_creation(self):
        """Create Bloom filter with optimal parameters."""
        config = BloomFilterConfig(1000, 0.01)
        bf = BloomFilter.create("test", config)
        
        assert bf.filter_id == "test"
        assert len(bf.bit_array) == config.optimal_bit_array_size
        assert bf.config.expected_elements == 1000
        assert bf.config.false_positive_rate == 0.01

    def test_bloom_filter_add_and_check(self):
        """Basic add and check operations."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        bf.add("hello")
        bf.add("world")
        
        assert "hello" in bf
        assert "world" in bf
        assert "goodbye" not in bf

    def test_bloom_filter_might_contain(self):
        """Explicit might_contain method."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        bf.add("test")
        assert bf.might_contain("test")
        assert not bf.might_contain("missing")

    def test_bloom_filter_false_positive_possible(self):
        """False positives are possible but rare with good config."""
        config = BloomFilterConfig(1000, 0.01)
        bf = BloomFilter.create("test", config)
        
        # Add many items
        for i in range(100):
            bf.add(f"item_{i}")
        
        # Test many non-existent items
        false_positives = 0
        for i in range(10000, 20000):
            if f"item_{i}" in bf:
                false_positives += 1
        
        # False positive rate should be low (< 5% with 1% target)
        fp_rate = false_positives / 10000
        assert fp_rate < 0.05  # Should be close to 1%

    def test_bloom_filter_stats(self):
        """Statistics tracking."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        bf.add("hello")
        bf.add("world")
        
        assert "hello" in bf
        assert "world" in bf
        assert "missing" not in bf
        
        stats = bf.stats
        assert stats.elements_added == 2
        assert stats.queries_made == 3
        assert stats.empirical_false_positive_rate == 0.0

    def test_bloom_filter_empty(self):
        """Empty filter check."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        assert bf.is_empty()
        bf.add("test")
        assert not bf.is_empty()

    def test_bloom_filter_fill_ratio(self):
        """Fill ratio calculation."""
        config = BloomFilterConfig(10, 0.1)  # Small filter for testing
        bf = BloomFilter.create("test", config)
        
        assert bf.fill_ratio() == 0.0
        bf.add("test")
        assert bf.fill_ratio() > 0.0
        assert bf.fill_ratio() <= 1.0

    def test_estimated_false_positive_rate(self):
        """Theoretical false positive rate estimation."""
        config = BloomFilterConfig(1000, 0.01)
        bf = BloomFilter.create("test", config)
        
        # Before adding anything
        assert bf.estimated_false_positive_rate() == 0.0
        
        # Add some elements
        for i in range(100):
            bf.add(f"item_{i}")
        
        fpr = bf.estimated_false_positive_rate()
        assert 0.0 < fpr < 1.0

    # =========================================================================
    # Repository Tests
    # =========================================================================

    def test_repository_save_load(self):
        """Repository save and load."""
        repo = InMemoryBloomFilterRepository()
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        bf.add("hello")
        
        repo.save(bf)
        loaded = repo.load("test")
        
        assert loaded is not None
        assert loaded.filter_id == "test"
        assert "hello" in loaded

    def test_repository_delete(self):
        """Repository delete."""
        repo = InMemoryBloomFilterRepository()
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        repo.save(bf)
        assert repo.load("test") is not None
        
        repo.delete("test")
        assert repo.load("test") is None

    # =========================================================================
    # Service Tests
    # =========================================================================

    def test_service_create_filter(self):
        """Service creates filter with optimal parameters."""
        repo = InMemoryBloomFilterRepository()
        service = BloomFilterService(repo)
        
        bf = service.create_filter("spell_check", 10000, 0.01)
        
        assert bf.filter_id == "spell_check"
        assert bf.config.expected_elements == 10000
        assert bf.config.false_positive_rate == 0.01

    def test_service_add_and_check(self):
        """Service add and check operations."""
        repo = InMemoryBloomFilterRepository()
        service = BloomFilterService(repo)
        
        service.create_filter("test", 100, 0.01)
        service.add_to_filter("test", "hello")
        
        assert service.check_filter("test", "hello") is True
        assert service.check_filter("test", "world") is False
        assert service.check_filter("nonexistent", "hello") is None

    def test_service_get_stats(self):
        """Service retrieves filter statistics."""
        repo = InMemoryBloomFilterRepository()
        service = BloomFilterService(repo)
        
        service.create_filter("test", 100, 0.01)
        service.add_to_filter("test", "hello")
        service.check_filter("test", "hello")
        
        stats = service.get_stats("test")
        assert stats is not None
        assert stats.elements_added == 1
        assert stats.queries_made == 1

    # =========================================================================
    # Facade Tests
    # =========================================================================

    def test_facade_create_filter(self):
        """Facade creates filter with optimal parameters."""
        bf = BloomFilters()
        filter_obj = bf.create_filter("test", 1000, 0.01)
        
        assert filter_obj.filter_id == "test"
        assert filter_obj.config.expected_elements == 1000

    def test_facade_add_and_check(self):
        """Facade add and check."""
        bf = BloomFilters()
        bf.create_filter("test", 100, 0.01)
        
        assert bf.add("test", "hello")
        assert bf.check("test", "hello") is True
        assert bf.check("test", "world") is False
        assert bf.check("nonexistent", "hello") is None

    def test_facade_stats(self):
        """Facade stats retrieval."""
        bf = BloomFilters()
        bf.create_filter("test", 100, 0.01)
        bf.add("test", "hello")
        bf.check("test", "hello")
        
        stats = bf.get_stats("test")
        assert stats is not None
        assert stats.elements_added == 1

    def test_facade_estimated_fpr(self):
        """Facade estimated FPR."""
        bf = BloomFilters()
        bf.create_filter("test", 1000, 0.01)
        
        for i in range(50):
            bf.add("test", f"item_{i}")
        
        fpr = bf.get_estimated_fpr("test")
        assert 0.0 < fpr < 1.0

    def test_facade_fill_ratio(self):
        """Facade fill ratio."""
        bf = BloomFilters()
        bf.create_filter("test", 100, 0.1)
        
        assert bf.get_fill_ratio("test") == 0.0
        bf.add("test", "hello")
        assert bf.get_fill_ratio("test") > 0.0

    # =========================================================================
    # Functional Interface Tests
    # =========================================================================

    def test_functional_bloom_filter(self):
        """Functional Bloom filter basic operations."""
        bf = BloomFilterFunctional(1000, 7)
        
        bf.add("hello")
        bf.add("world")
        
        assert "hello" in bf
        assert "world" in bf
        assert "goodbye" not in bf

    def test_functional_add_multiple(self):
        """Functional add_multiple."""
        bf = BloomFilterFunctional(1000, 7)
        
        bf.add_multiple(["apple", "banana", "cherry"])
        
        assert "apple" in bf
        assert "banana" in bf
        assert "cherry" in bf

    def test_functional_check_multiple(self):
        """Functional check_multiple."""
        bf = BloomFilterFunctional(1000, 7)
        bf.add_multiple(["a", "b", "c"])
        
        results = bf.check_multiple(["a", "b", "d", "c"])
        assert results == [True, True, False, True]

    def test_create_bloom_filter_factory(self):
        """Factory function creates filter with optimal params."""
        bf = create_bloom_filter(1000, 0.01)
        
        assert isinstance(bf, BloomFilterFunctional)
        assert bf.m in (9585, 9586)  # Optimal bit array size
        assert bf.k == 7     # Optimal hash count

    # =========================================================================
    # Hash Function Property Tests
    # =========================================================================

    def test_hash_distribution(self):
        """Hash functions should distribute uniformly."""
        hf = MD5HashFunction()
        m = 1000
        counts = [0] * m
        
        for i in range(10000):
            idx = hf.hash(f"item_{i}", 0, m)
            counts[idx] += 1
        
        # Check rough uniformity (no bucket should have > 3x expected)
        expected = 10000 / 1000
        for count in counts:
            assert count < expected * 3

    def test_double_hash_distribution(self):
        """Double hashing should distribute uniformly."""
        dh = DoubleHashFunction()
        m = 1000
        k = 7
        counts = [0] * m
        
        for i in range(1000):
            indices = dh.hash_k(f"item_{i}", k, m)
            for idx in indices:
                counts[idx] += 1
        
        expected = 7000 / 1000
        for count in counts:
            assert count < expected * 3

    # =========================================================================
    # Edge Cases
    # =========================================================================

    def test_empty_string(self):
        """Empty string should work."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        bf.add("")
        assert "" in bf

    def test_unicode_strings(self):
        """Unicode strings should work."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        bf.add("hello")
        bf.add("世界")
        bf.add("🌍")
        
        assert "hello" in bf
        assert "世界" in bf
        assert "🌍" in bf

    def test_very_long_strings(self):
        """Very long strings should work."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        long_string = "a" * 10000
        bf.add(long_string)
        assert long_string in bf

    def test_duplicate_adds(self):
        """Adding same item multiple times should be idempotent."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        for _ in range(10):
            bf.add("test")
        
        assert "test" in bf
        assert bf.stats.elements_added == 10  # Each add counts

    def test_case_sensitivity(self):
        """Bloom filter should be case-sensitive."""
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        bf.add("Hello")
        assert "Hello" in bf
        assert "hello" not in bf
        assert "HELLO" not in bf

    # =========================================================================
    # Architecture Pattern Tests
    # =========================================================================

    def test_cqrs_separation(self):
        """Commands and queries are separated."""
        bf = BloomFilters()
        
        # Commands modify state
        bf.create_filter("test", 100, 0.01)
        bf.add("test", "hello")
        
        # Queries read state
        assert bf.check("test", "hello") is True
        assert bf.check("test", "world") is False

    def test_repository_pattern(self):
        """Repository abstracts storage."""
        repo = InMemoryBloomFilterRepository()
        config = BloomFilterConfig(100, 0.01)
        bf = BloomFilter.create("test", config)
        
        repo.save(bf)
        loaded = repo.load("test")
        assert loaded is not None

    def test_domain_service_encapsulation(self):
        """BloomFilterService encapsulates business logic."""
        repo = InMemoryBloomFilterRepository()
        service = BloomFilterService(repo)
        
        bf = service.create_filter("test", 100, 0.01)
        assert service.add_to_filter("test", "hello")
        assert service.check_filter("test", "hello") is True

    # =========================================================================
    # Functional Interface Tests
    # =========================================================================

    def test_functional_create_bloom_filter(self):
        """Factory function creates properly configured filter."""
        bf = create_bloom_filter(1000, 0.01)
        
        assert isinstance(bf, BloomFilterFunctional)
        assert bf.m in (9585, 9586)
        assert bf.k == 7

    def test_functional_interface_compatibility(self):
        """Functional interface should work like built-in set."""
        bf = create_bloom_filter(1000, 0.01)
        
        bf.add("test")
        assert "test" in bf
        assert "other" not in bf

    def test_multiple_filters_independent(self):
        """Multiple filters should be independent."""
        bf = BloomFilters()
        
        bf.create_filter("filter1", 100, 0.01)
        bf.create_filter("filter2", 100, 0.01)
        
        bf.add("filter1", "hello")
        bf.add("filter2", "world")
        
        assert "hello" in bf._repository.load("filter1")
        assert "hello" not in bf._repository.load("filter2")
        assert "world" in bf._repository.load("filter2")
        assert "world" not in bf._repository.load("filter1")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])