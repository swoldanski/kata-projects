"""Tests for Kata02: Karate Chop - Binary Search with 5 Implementations."""

import pytest
from kata02_karate_chop import (
    BinarySearchService,
    InMemorySearchHistoryRepository,
    KarateChop,
    SearchAlgorithm,
    SearchResult,
    chop,
    chop_builtin,
    chop_functional,
    chop_iterative,
    chop_recursive,
    chop_tail_recursive,
)

ALL_CHOP_IMPLEMENTATIONS = [
    chop_iterative,
    chop_recursive,
    chop_functional,
    chop_builtin,
    chop_tail_recursive,
]


class TestKarateChop:
    """Test cases for Kata02: Karate Chop."""

    def setup_method(self):
        """Create a fresh KarateChop instance for each test."""
        self.kc = KarateChop()
        self.arr = [1, 3, 5, 7, 9, 11, 13, 15]

    # =========================================================================
    # Basic Cases from README Examples
    # =========================================================================

    def test_chop_empty_array(self):
        """chop(3, []) => -1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(3, []) == -1

    def test_chop_single_element_not_found(self):
        """chop(3, [1]) => -1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(3, [1]) == -1

    def test_chop_single_element_found(self):
        """chop(1, [1]) => 0"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(1, [1]) == 0

    def test_chop_first_element(self):
        """chop(1, [1, 3, 5]) => 0"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(1, [1, 3, 5]) == 0

    def test_chop_middle_element(self):
        """chop(3, [1, 3, 5]) => 1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(3, [1, 3, 5]) == 1

    def test_chop_last_element(self):
        """chop(5, [1, 3, 5]) => 2"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(5, [1, 3, 5]) == 2

    def test_chop_before_first(self):
        """chop(0, [1, 3, 5]) => -1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(0, [1, 3, 5]) == -1

    def test_chop_between_first_and_second(self):
        """chop(2, [1, 3, 5]) => -1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(2, [1, 3, 5]) == -1

    def test_chop_between_second_and_third(self):
        """chop(4, [1, 3, 5]) => -1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(4, [1, 3, 5]) == -1

    def test_chop_after_last(self):
        """chop(6, [1, 3, 5]) => -1"""
        for func in ALL_CHOP_IMPLEMENTATIONS:
            assert func(6, [1, 3, 5]) == -1

    # =========================================================================
    # Larger Array Tests
    # =========================================================================

    def test_chop_first_in_larger_array(self):
        """First element in larger array."""
        assert chop(1, self.arr) == 0

    def test_chop_middle_in_larger_array(self):
        """Middle element in larger array."""
        assert chop(9, self.arr) == 4

    def test_chop_last_in_larger_array(self):
        """Last element in larger array."""
        assert chop(15, self.arr) == 7

    def test_chop_not_found_in_larger_array(self):
        """Element not in larger array."""
        assert chop(8, self.arr) == -1
        assert chop(16, self.arr) == -1
        assert chop(0, self.arr) == -1

    # =========================================================================
    # All 5 Implementations Produce Same Results
    # =========================================================================

    def test_all_implementations_match(self):
        """All 5 implementations should return identical results for all test cases."""
        test_cases = [
            (3, []),
            (3, [1]),
            (1, [1]),
            (1, [1, 3, 5]),
            (3, [1, 3, 5]),
            (5, [1, 3, 5]),
            (0, [1, 3, 5]),
            (2, [1, 3, 5]),
            (4, [1, 3, 5]),
            (6, [1, 3, 5]),
            (1, [1, 3, 5, 7, 9]),
            (9, [1, 3, 5, 7, 9]),
            (5, [1, 3, 5, 7, 9]),
            (0, [1, 3, 5, 7, 9]),
            (10, [1, 3, 5, 7, 9]),
        ]

        functions = ALL_CHOP_IMPLEMENTATIONS

        for target, test_arr in test_cases:
            results = [f(target, test_arr) for f in functions]
            # All should be equal
            assert all(r == results[0] for r in results), (
                f"Mismatch for chop({target}, {test_arr}): {results}"
            )

    # =========================================================================
    # SearchResult Details
    # =========================================================================

    def test_search_result_contains_metadata(self):
        """SearchResult should contain index, algorithm, iterations, comparisons."""
        result = self.kc.search_one(3, self.arr, SearchAlgorithm.ITERATIVE)
        assert isinstance(result, SearchResult)
        assert result.index == 1
        assert result.algorithm == SearchAlgorithm.ITERATIVE
        assert result.iterations > 0
        assert result.comparisons > 0

    def test_iterative_search_result(self):
        """Iterative search should have correct metadata."""
        result = self.kc.search_one(3, self.arr, SearchAlgorithm.ITERATIVE)
        assert result.algorithm == SearchAlgorithm.ITERATIVE
        assert result.index == 1
        assert result.iterations >= 1

    def test_recursive_search_result(self):
        """Recursive search should have correct metadata."""
        result = self.kc.search_one(3, self.arr, SearchAlgorithm.RECURSIVE)
        assert result.algorithm == SearchAlgorithm.RECURSIVE
        assert result.index == 1

    def test_functional_search_result(self):
        """Functional search should have correct metadata."""
        result = self.kc.search_one(3, self.arr, SearchAlgorithm.FUNCTIONAL)
        assert result.algorithm == SearchAlgorithm.FUNCTIONAL
        assert result.index == 1

    def test_builtin_search_result(self):
        """Built-in search should have correct metadata."""
        result = self.kc.search_one(3, self.arr, SearchAlgorithm.BUILTIN)
        assert result.algorithm == SearchAlgorithm.BUILTIN
        assert result.index == 1
        assert result.iterations == 1  # bisect counts as 1

    def test_tail_recursive_search_result(self):
        """Tail-recursive search should have correct metadata."""
        result = self.kc.search_one(3, self.arr, SearchAlgorithm.TAIL_RECURSIVE)
        assert result.algorithm == SearchAlgorithm.TAIL_RECURSIVE
        assert result.index == 1

    # =========================================================================
    # Edge Cases
    # =========================================================================

    def test_empty_array_all_algorithms(self):
        """Empty array should return -1 for all algorithms."""
        for algo in SearchAlgorithm:
            result = self.kc.search_one(5, [], algo)
            assert result.index == -1

    def test_single_element_array(self):
        """Single element array edge cases."""
        for algo in SearchAlgorithm:
            assert self.kc.search_one(1, [1], algo).index == 0
            assert self.kc.search_one(2, [1], algo).index == -1

    def test_two_element_array(self):
        """Two element array."""
        arr = [1, 3]
        for algo in SearchAlgorithm:
            assert self.kc.search_one(1, arr, algo).index == 0
            assert self.kc.search_one(3, arr, algo).index == 1
            assert self.kc.search_one(2, arr, algo).index == -1
            assert self.kc.search_one(0, arr, algo).index == -1
            assert self.kc.search_one(4, arr, algo).index == -1

    # =========================================================================
    # TDD Progression - Following Kata Steps
    # =========================================================================

    def test_tdd_step_1_empty_array(self):
        """Step 1: Empty array returns -1."""
        assert chop(3, []) == -1

    def test_tdd_step_2_single_element_not_found(self):
        """Step 2: Single element, not found."""
        assert chop(3, [1]) == -1

    def test_tdd_step_3_single_element_found(self):
        """Step 3: Single element, found."""
        assert chop(1, [1]) == 0

    def test_tdd_step_4_first_element(self):
        """Step 4: First element of 3."""
        assert chop(1, [1, 3, 5]) == 0

    def test_tdd_step_5_middle_element(self):
        """Step 5: Middle element of 3."""
        assert chop(3, [1, 3, 5]) == 1

    def test_tdd_step_6_last_element(self):
        """Step 6: Last element of 3."""
        assert chop(5, [1, 3, 5]) == 2

    def test_tdd_step_7_before_first(self):
        """Step 7: Before first element."""
        assert chop(0, [1, 3, 5]) == -1

    def test_tdd_step_8_between_elements(self):
        """Step 8: Between elements."""
        assert chop(2, [1, 3, 5]) == -1
        assert chop(4, [1, 3, 5]) == -1

    def test_tdd_step_9_after_last(self):
        """Step 9: After last element."""
        assert chop(6, [1, 3, 5]) == -1

    # =========================================================================
    # Facade Tests
    # =========================================================================

    def test_search_all_returns_all_algorithms(self):
        """search_all should return results for all 5 algorithms."""
        results = self.kc.search_all(3, [1, 3, 5])
        assert len(results) == 5
        algorithms = {r.algorithm for r in results}
        assert algorithms == set(SearchAlgorithm)

    def test_search_with_specific_algorithm(self):
        """search with specific algorithm returns single result."""
        result = self.kc.search(3, [1, 3, 5], SearchAlgorithm.RECURSIVE)
        assert len(result.results) == 1
        assert result.results[0].algorithm == SearchAlgorithm.RECURSIVE

    def test_search_without_algorithm_returns_all(self):
        """search without algorithm returns all."""
        result = self.kc.search(3, [1, 3, 5])
        assert len(result.results) == 5

    def test_history_tracking(self):
        """Search history should be tracked."""
        self.kc.search_one(3, self.arr, SearchAlgorithm.ITERATIVE)
        self.kc.search_one(5, self.arr, SearchAlgorithm.ITERATIVE)
        self.kc.search_one(7, self.arr, SearchAlgorithm.RECURSIVE)

        history = self.kc.get_history()
        assert len(history) == 3

        iterative_history = self.kc.get_history(SearchAlgorithm.ITERATIVE)
        assert len(iterative_history) == 2

    def test_stats_tracking(self):
        """Statistics should be tracked."""
        self.kc.search_one(3, self.arr, SearchAlgorithm.ITERATIVE)
        self.kc.search_one(5, self.arr, SearchAlgorithm.ITERATIVE)

        stats = self.kc.get_stats(SearchAlgorithm.ITERATIVE)
        assert stats["count"] == 2
        assert stats["avg_iterations"] > 0
        assert stats["avg_comparisons"] > 0

    def test_cqrs_separation(self):
        """Commands and queries should be separated."""
        # Write through command handler (record search)
        self.kc.record_search(3, self.arr, SearchAlgorithm.ITERATIVE)
        # Read through query handler
        result = self.kc.search(3, self.arr, SearchAlgorithm.ITERATIVE)
        assert len(result.results) == 1

    # =========================================================================
    # Architecture Pattern Tests
    # =========================================================================

    def test_repository_pattern(self):
        """InMemorySearchHistoryRepository should work."""
        repo = InMemorySearchHistoryRepository()
        result = SearchResult(1, SearchAlgorithm.ITERATIVE, 2, 3)
        repo.save(result)
        assert repo.get_history() == [result]
        assert repo.get_stats()["count"] == 1

    def test_domain_service_encapsulation(self):
        """BinarySearchService should encapsulate all algorithms."""
        repo = InMemorySearchHistoryRepository()
        service = BinarySearchService(repo)

        # All algorithms accessible
        for algo in SearchAlgorithm:
            result = service.search(3, [1, 3, 5], algo)
            assert result.index == 1
            assert result.algorithm == algo

    def test_service_search_all(self):
        """Service search_all should return all algorithms."""
        repo = InMemorySearchHistoryRepository()
        service = BinarySearchService(repo)
        results = service.search_all(3, [1, 3, 5])
        assert len(results) == 5

    # =========================================================================
    # Functional Interface Tests
    # =========================================================================

    def test_chop_function_is_iterative(self):
        """chop() convenience function should use iterative."""
        assert chop(3, [1, 3, 5]) == 1
        assert chop(0, [1, 3, 5]) == -1

    def test_individual_functions(self):
        """Each individual function should work."""
        assert chop_iterative(3, [1, 3, 5]) == 1
        assert chop_recursive(3, [1, 3, 5]) == 1
        assert chop_functional(3, [1, 3, 5]) == 1
        assert chop_builtin(3, [1, 3, 5]) == 1
        assert chop_tail_recursive(3, [1, 3, 5]) == 1

    # =========================================================================
    # Performance / Correctness Properties
    # =========================================================================

    def test_binary_search_correctness_property(self):
        """For any sorted array, if element exists, returned index should have that value."""
        import random

        # Test with various sorted arrays
        for size in [1, 2, 3, 5, 10, 20, 50, 100]:
            arr = list(range(0, size * 2, 2))  # Even numbers: 0, 2, 4, ...
            for _ in range(10):
                target = random.choice(arr)
                for func in ALL_CHOP_IMPLEMENTATIONS:
                    idx = func(target, arr)
                    assert idx != -1
                    assert arr[idx] == target

    def test_not_found_returns_negative_one(self):
        """If target not in array, should return -1."""
        arr = list(range(100))
        for target in [-1, 100, 101, 150]:  # All not in [0..99]
            for func in ALL_CHOP_IMPLEMENTATIONS:
                assert func(int(target), arr) == -1

    def test_all_algorithms_handle_duplicates_consistently(self):
        """With duplicates, should return some valid index (binary search finds one)."""
        arr = [1, 2, 2, 2, 3, 4, 5]
        target = 2
        results = [f(target, arr) for f in ALL_CHOP_IMPLEMENTATIONS]
        # All should find some index with value 2
        for idx in results:
            assert idx != -1
            assert arr[idx] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])