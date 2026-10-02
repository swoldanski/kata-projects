"""Tests for Kata03: How Big? How Fast? - Estimation Calculator."""

import pytest
from math import log2, ceil
from kata03_how_big_how_fast import (
    HowBigHowFast,
    estimate_bits,
    estimate_bits_range,
    estimate_town_records_storage,
    estimate_binary_tree_storage,
    estimate_modem_transfer_time,
    estimate_binary_search_time,
    estimate_password_cracking_time,
    get_kata_answers,
    BitEstimate,
    StorageEstimate,
    TimeEstimate,
    EstimationCategory,
    InMemoryEstimationRepository,
    BitEstimationService,
    StorageEstimationService,
    TimeEstimationService,
)


class TestHowBigHowFast:
    """Test cases for Kata03: How Big? How Fast?."""

    def setup_method(self):
        """Create a fresh calculator for each test."""
        self.calc = HowBigHowFast()

    # =========================================================================
    # Basic Cases - Bits for Unsigned Representation
    # =========================================================================

    def test_estimate_bits_for_1000(self):
        """Bits for 1,000."""
        result = self.calc.estimate_bits(1_000)
        assert isinstance(result, BitEstimate)
        assert result.exact_bits == 10  # 2^10 = 1024 > 1000
        assert result.value == 1_000

    def test_estimate_bits_for_1_million(self):
        """Bits for 1,000,000."""
        result = self.calc.estimate_bits(1_000_000)
        assert result.exact_bits == 20  # 2^20 = 1,048,576 > 1,000,000

    def test_estimate_bits_for_1_billion(self):
        """Bits for 1,000,000,000."""
        result = self.calc.estimate_bits(1_000_000_000)
        assert result.exact_bits == 30  # 2^30 = 1,073,741,824 > 1B

    def test_estimate_bits_for_1_trillion(self):
        """Bits for 1,000,000,000,000."""
        result = self.calc.estimate_bits(1_000_000_000_000)
        assert result.exact_bits == 40  # 2^40 ≈ 1.1T > 1T

    def test_estimate_bits_for_8_trillion(self):
        """Bits for 8,000,000,000,000."""
        result = self.calc.estimate_bits(8_000_000_000_000)
        assert result.exact_bits == 43  # 2^43 ≈ 8.8T > 8T

    def test_estimate_bits_zero(self):
        """Zero requires 0 bits."""
        result = self.calc.estimate_bits(0)
        assert result.exact_bits == 0

    def test_estimate_bits_negative(self):
        """Negative numbers return 0 bits."""
        result = self.calc.estimate_bits(-1)
        assert result.exact_bits == 0

    # =========================================================================
    # Functional Interface - Bits
    # =========================================================================

    def test_functional_estimate_bits(self):
        """Functional estimate_bits should match class method."""
        for n in [0, 1, 10, 100, 1000, 1_000_000]:
            expected = ceil(log2(n + 1)) if n > 0 else 0
            assert estimate_bits(n) == expected

    def test_functional_estimate_bits_range(self):
        """Functional estimate_bits_range."""
        assert estimate_bits_range(1000) == 10
        assert estimate_bits_range(1_000_000) == 20

    # =========================================================================
    # Storage Estimations - Town Records
    # =========================================================================

    def test_town_records_20k(self):
        """20,000 town records storage."""
        result = self.calc.estimate_town_records(20_000)
        assert isinstance(result, StorageEstimate)
        # 20,000 * 95 chars = 1,900,000 bytes ≈ 1.9 MB
        assert result.bytes == 1_900_000
        assert "MB" in result.human_readable

    def test_town_records_custom_fields(self):
        """Town records with custom field sizes."""
        result = self.calc.estimate_town_records(
            10_000, chars_per_name=20, chars_per_address=40, chars_per_phone=10
        )
        # 10,000 * (20+40+10) = 700,000 bytes
        assert result.bytes == 700_000

    def test_functional_town_records(self):
        """Functional town records estimation."""
        assert estimate_town_records_storage(20_000) == 1_900_000
        assert estimate_town_records_storage(10_000) == 950_000

    # =========================================================================
    # Storage Estimations - Binary Tree
    # =========================================================================

    def test_binary_tree_32bit(self):
        """Binary tree storage on 32-bit."""
        result = self.calc.estimate_binary_tree(1_000_000, is_64bit=False)
        assert isinstance(result, StorageEstimate)
        # 1M nodes * (4 + 3*4 + 16) = 1M * 32 = 32 MB
        assert result.bytes == 32_000_000
        assert "MB" in result.human_readable
        assert "32-bit" in result.breakdown

    def test_binary_tree_64bit(self):
        """Binary tree storage on 64-bit."""
        result = self.calc.estimate_binary_tree(1_000_000, is_64bit=True)
        assert result.bytes == 56_000_000  # 1M * (4 + 3*8 + 24) = 56 MB
        assert "64-bit" in result.breakdown

    def test_functional_binary_tree(self):
        """Functional binary tree estimation."""
        assert estimate_binary_tree_storage(1_000_000, False) == 32_000_000
        assert estimate_binary_tree_storage(1_000_000, True) == 52_000_000

    # =========================================================================
    # Time Estimations - Modem Transfer
    # =========================================================================

    def test_modem_transfer_1200_pages(self):
        """1,200 pages over 56k baud modem."""
        result = self.calc.estimate_modem_transfer(1_200)
        assert isinstance(result, TimeEstimate)
        # 1200 * 2000 * 8 / 56000 ≈ 342.86 seconds ≈ 5.7 minutes
        assert result.milliseconds > 300_000  # > 5 minutes
        assert result.milliseconds < 400_000  # < 6.7 minutes

    def test_functional_modem_transfer(self):
        """Functional modem transfer time."""
        secs = estimate_modem_transfer_time(1_200)
        assert 300 < secs < 400

    # =========================================================================
    # Time Estimations - Binary Search Scaling
    # =========================================================================

    def test_binary_search_scaling(self):
        """Binary search time for 10M elements."""
        result = self.calc.estimate_binary_search_time(4.5, 6.0, 10_000_000)
        assert isinstance(result, TimeEstimate)
        # log2(10M) ≈ 23.25, k ≈ (4.5/13.29 + 6.0/16.61)/2 ≈ 0.34
        # estimated ≈ 0.34 * 23.25 ≈ 7.9 ms
        assert 7 < result.milliseconds < 10

    def test_functional_binary_search(self):
        """Functional binary search scaling."""
        result = estimate_binary_search_time(4.5, 6.0, 10_000_000)
        assert 7 < result < 10

    def test_binary_search_scaling_properties(self):
        """Binary search should scale logarithmically."""
        t1 = self.calc.estimate_binary_search_time(4.5, 6.0, 10_000)
        t2 = self.calc.estimate_binary_search_time(4.5, 6.0, 100_000)
        t3 = self.calc.estimate_binary_search_time(4.5, 6.0, 10_000_000)
        
        # Times should increase with n
        assert t1.milliseconds < t2.milliseconds < t3.milliseconds
        
        # Ratio of times should approximate log ratio
        ratio_100k_10k = t2.milliseconds / t1.milliseconds
        ratio_10m_100k = t3.milliseconds / t2.milliseconds
        
        # log2(100k)/log2(10k) ≈ 16.61/13.29 ≈ 1.25
        # log2(10M)/log2(100k) ≈ 23.25/16.61 ≈ 1.40
        assert 1.2 < ratio_100k_10k < 1.3
        assert 1.3 < ratio_10m_100k < 1.5

    def test_functional_binary_search(self):
        """Functional binary search time."""
        result = estimate_binary_search_time(4.5, 6.0, 10_000_000)
        assert 7 < result < 10

    # =========================================================================
    # Time Estimations - Password Cracking
    # =========================================================================

    def test_password_cracking(self):
        """Password cracking estimation."""
        result = self.calc.estimate_password_cracking(16, 96, 1.0)
        assert isinstance(result, TimeEstimate)
        # 96^16 is astronomically large
        # Should be many years
        assert "years" in result.human_readable

    def test_password_cracking_short(self):
        """Short password cracking."""
        result = self.calc.estimate_password_cracking(4, 26, 1.0)  # 4 chars, lowercase
        # 26 + 26^2 + 26^3 + 26^4 = 26 + 676 + 17576 + 456976 = 475,254
        # 475,254 ms ≈ 7.9 minutes
        assert "minute" in result.human_readable.lower() or "second" in result.human_readable.lower()

    def test_functional_password_cracking(self):
        """Functional password cracking time."""
        result = estimate_password_cracking_time(16, 96, 1.0)
        # Should be enormous
        assert result > 1e20  # Very large number of ms

    # =========================================================================
    # Kata Answers
    # =========================================================================

    def test_get_kata_answers_structure(self):
        """get_kata_answers should return all answers."""
        answers = get_kata_answers()
        
        assert "bits" in answers
        assert "town_records" in answers
        assert "binary_tree_32bit" in answers
        assert "binary_tree_64bit" in answers
        assert "modem_transfer" in answers
        assert "binary_search_10m" in answers
        assert "password_cracking" in answers
        
        # Check bits answers
        assert 1_000 in answers["bits"]
        assert 1_000_000 in answers["bits"]
        assert 1_000_000_000 in answers["bits"]
        assert 1_000_000_000_000 in answers["bits"]
        assert 8_000_000_000_000 in answers["bits"]

    def test_kata_answers_values(self):
        """Check specific kata answer values."""
        answers = get_kata_answers()
        
        # Bits
        assert "10 bits" in answers["bits"][1_000]
        assert "20 bits" in answers["bits"][1_000_000]
        assert "30 bits" in answers["bits"][1_000_000_000]
        assert "40 bits" in answers["bits"][1_000_000_000_000]
        assert "43 bits" in answers["bits"][8_000_000_000_000]

    # =========================================================================
    # Repository & History
    # =========================================================================

    def test_history_tracking(self):
        """History should be tracked."""
        self.calc.estimate_bits(1000)
        self.calc.estimate_town_records(20000)
        
        history = self.calc.get_history()
        assert len(history) == 2
        
        bits_history = self.calc.get_history(EstimationCategory.BITS)
        assert len(bits_history) == 1
        
        storage_history = self.calc.get_history(EstimationCategory.STORAGE)
        assert len(storage_history) == 1

    def test_clear_history(self):
        """Clear history should work."""
        self.calc.estimate_bits(1000)
        self.calc.clear_history()
        assert len(self.calc.get_history()) == 0

    def test_repository_pattern(self):
        """In-memory repository should work."""
        repo = InMemoryEstimationRepository()
        repo.save(EstimationCategory.BITS, "1000", BitEstimate(1000, 10, "test"))
        assert len(repo.get_history()) == 1
        repo.clear()
        assert len(repo.get_history()) == 0

    # =========================================================================
    # Architecture Pattern Tests
    # =========================================================================

    def test_cqrs_separation(self):
        """Commands and queries should be separated."""
        # Commands modify state (history)
        self.calc.estimate_bits(1000)
        self.calc.estimate_bits(2000)
        
        # Queries read state
        history = self.calc.get_history(EstimationCategory.BITS)
        assert len(history) == 2

    def test_domain_services_encapsulation(self):
        """Estimation logic should be in domain services."""
        # Bit estimation
        bit_result = BitEstimationService.bits_for_unsigned(1_000_000)
        assert bit_result.exact_bits == 20
        
        # Storage estimation
        storage_result = StorageEstimationService.estimate_town_records(20_000)
        assert storage_result.bytes == 1_900_000
        
        # Time estimation
        time_result = TimeEstimationService.estimate_modem_transfer(1_200)
        assert time_result.milliseconds > 300_000

    # =========================================================================
    # Edge Cases
    # =========================================================================

    def test_large_numbers(self):
        """Very large numbers should work."""
        result = self.calc.estimate_bits(10**100)
        assert result.exact_bits > 300

    def test_estimation_categories(self):
        """All estimation categories should be available."""
        assert EstimationCategory.BITS
        assert EstimationCategory.STORAGE
        assert EstimationCategory.TIME


if __name__ == "__main__":
    pytest.main([__file__, "-v"])