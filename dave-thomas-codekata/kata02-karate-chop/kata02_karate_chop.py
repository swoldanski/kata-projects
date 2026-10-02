"""Kata02: Karate Chop - Binary Search with 5 Implementations

This module implements 5 unique binary search algorithms following
DDD/CQRS/Repository patterns with in-memory state.

Source: http://codekata.com/kata/kata02-karate-chop/

The kata requires 5 totally unique implementations:
1. Traditional iterative
2. Recursive
3. Functional style with array slices
4. Using built-in library (bisect)
5. Tail-recursive
"""

from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

# =============================================================================
# Value Objects / Types
# =============================================================================

class SearchAlgorithm(Enum):
    ITERATIVE = "iterative"
    RECURSIVE = "recursive"
    FUNCTIONAL = "functional"
    BUILTIN = "builtin"
    TAIL_RECURSIVE = "tail_recursive"


@dataclass(frozen=True)
class SearchResult:
    """Result of a binary search."""
    index: int              # -1 if not found
    algorithm: SearchAlgorithm
    iterations: int         # Number of loop iterations / recursive calls
    comparisons: int        # Number of element comparisons made


# =============================================================================
# Repository Interface (for search history / statistics)
# =============================================================================

class SearchHistoryRepository(Protocol):
    """Repository for tracking search history."""

    def save(self, result: SearchResult) -> None: ...

    def get_history(self, algorithm: SearchAlgorithm | None = None) -> list[SearchResult]: ...

    def get_stats(self, algorithm: SearchAlgorithm | None = None) -> dict: ...


class InMemorySearchHistoryRepository:
    """In-memory implementation of search history repository."""

    def __init__(self):
        self._history: list[SearchResult] = []

    def save(self, result: SearchResult) -> None:
        self._history.append(result)

    def get_history(self, algorithm: SearchAlgorithm | None = None) -> list[SearchResult]:
        if algorithm:
            return [r for r in self._history if r.algorithm == algorithm]
        return list(self._history)

    def get_stats(self, algorithm: SearchAlgorithm | None = None) -> dict:
        history = self.get_history(algorithm)
        if not history:
            return {"count": 0, "avg_iterations": 0, "avg_comparisons": 0}
        return {
            "count": len(history),
            "avg_iterations": sum(r.iterations for r in history) / len(history),
            "avg_comparisons": sum(r.comparisons for r in history) / len(history),
        }


# =============================================================================
# Domain Service - Binary Search Implementations
# =============================================================================

class BinarySearchService:
    """Domain service containing all 5 binary search implementations."""

    def __init__(self, history_repo: SearchHistoryRepository | None = None):
        self._history_repo = history_repo or InMemorySearchHistoryRepository()

    # -------------------------------------------------------------------------
    # Implementation 1: Traditional Iterative
    # -------------------------------------------------------------------------
    def search_iterative(self, target: int, arr: list[int]) -> SearchResult:
        """Traditional iterative binary search.
        
        Uses low/high pointers, loop until found or exhausted.
        """
        low = 0
        high = len(arr) - 1
        iterations = 0
        comparisons = 0

        while low <= high:
            iterations += 1
            mid = (low + high) // 2
            comparisons += 1

            if arr[mid] == target:
                result = SearchResult(mid, SearchAlgorithm.ITERATIVE, iterations, comparisons)
                self._history_repo.save(result)
                return result
            elif arr[mid] < target:
                comparisons += 1  # for the elif check
                low = mid + 1
            else:
                comparisons += 1  # for the else branch
                high = mid - 1

        result = SearchResult(-1, SearchAlgorithm.ITERATIVE, iterations, comparisons)
        self._history_repo.save(result)
        return result

    # -------------------------------------------------------------------------
    # Implementation 2: Recursive
    # -------------------------------------------------------------------------
    def search_recursive(self, target: int, arr: list[int]) -> SearchResult:
        """Recursive binary search.
        
        Recursively searches left or right half.
        """
        def _recursive(low: int, high: int, iterations: int, comparisons: int) -> SearchResult:
            if low > high:
                return SearchResult(-1, SearchAlgorithm.RECURSIVE, iterations, comparisons)

            iterations += 1
            mid = (low + high) // 2
            comparisons += 1

            if arr[mid] == target:
                return SearchResult(mid, SearchAlgorithm.RECURSIVE, iterations, comparisons)
            elif arr[mid] < target:
                return _recursive(mid + 1, high, iterations, comparisons + 1)
            else:
                return _recursive(low, mid - 1, iterations, comparisons + 1)

        result = _recursive(0, len(arr) - 1, 0, 0)
        self._history_repo.save(result)
        return result

    # -------------------------------------------------------------------------
    # Implementation 3: Functional Style (Array Slices)
    # -------------------------------------------------------------------------
    def search_functional(self, target: int, arr: list[int]) -> SearchResult:
        """Functional style using array slices.
        
        Passes sub-arrays instead of indices. Less efficient due to slicing
        but demonstrates functional approach.
        """
        def _functional(
            sub_arr: list[int], offset: int, iterations: int, comparisons: int
        ) -> SearchResult:
            if not sub_arr:
                return SearchResult(-1, SearchAlgorithm.FUNCTIONAL, iterations, comparisons)

            iterations += 1
            mid = len(sub_arr) // 2
            comparisons += 1

            if sub_arr[mid] == target:
                return SearchResult(
                    offset + mid, SearchAlgorithm.FUNCTIONAL, iterations, comparisons
                )
            elif sub_arr[mid] < target:
                # Right half: slice and adjust offset
                return _functional(sub_arr[mid + 1:], offset + mid + 1, iterations, comparisons + 1)
            else:
                # Left half: slice, offset unchanged
                return _functional(sub_arr[:mid], offset, iterations, comparisons + 1)

        result = _functional(arr, 0, 0, 0)
        self._history_repo.save(result)
        return result

    # -------------------------------------------------------------------------
    # Implementation 4: Built-in (bisect)
    # -------------------------------------------------------------------------
    def search_builtin(self, target: int, arr: list[int]) -> SearchResult:
        """Using Python's bisect module.
        
        bisect_left returns insertion point; check if target exists there.
        """
        iterations = 1  # bisect is O(log n) but we count as 1 "iteration"
        comparisons = 1  # one comparison to verify

        index = bisect_left(arr, target)

        if index < len(arr) and arr[index] == target:
            result = SearchResult(index, SearchAlgorithm.BUILTIN, iterations, comparisons)
        else:
            result = SearchResult(-1, SearchAlgorithm.BUILTIN, iterations, comparisons)

        self._history_repo.save(result)
        return result

    # -------------------------------------------------------------------------
    # Implementation 5: Tail-Recursive
    # -------------------------------------------------------------------------
    def search_tail_recursive(self, target: int, arr: list[int]) -> SearchResult:
        """Tail-recursive binary search.
        
        Recursive call is the last operation; some languages optimize this.
        Python doesn't optimize tail calls, but this demonstrates the pattern.
        """
        def _tail_recursive(low: int, high: int, iterations: int, comparisons: int) -> SearchResult:
            # Tail call - no computation after recursive call
            if low > high:
                return SearchResult(-1, SearchAlgorithm.TAIL_RECURSIVE, iterations, comparisons)

            iterations += 1
            mid = (low + high) // 2
            comparisons += 1

            if arr[mid] == target:
                return SearchResult(mid, SearchAlgorithm.TAIL_RECURSIVE, iterations, comparisons)
            elif arr[mid] < target:
                return _tail_recursive(mid + 1, high, iterations, comparisons + 1)
            else:
                return _tail_recursive(low, mid - 1, iterations, comparisons + 1)

        result = _tail_recursive(0, len(arr) - 1, 0, 0)
        self._history_repo.save(result)
        return result

    # -------------------------------------------------------------------------
    # Unified interface
    # -------------------------------------------------------------------------
    def search(self, target: int, arr: list[int], algorithm: SearchAlgorithm) -> SearchResult:
        """Dispatch to the selected algorithm."""
        dispatch = {
            SearchAlgorithm.ITERATIVE: self.search_iterative,
            SearchAlgorithm.RECURSIVE: self.search_recursive,
            SearchAlgorithm.FUNCTIONAL: self.search_functional,
            SearchAlgorithm.BUILTIN: self.search_builtin,
            SearchAlgorithm.TAIL_RECURSIVE: self.search_tail_recursive,
        }
        return dispatch[algorithm](target, arr)

    def search_all(self, target: int, arr: list[int]) -> list[SearchResult]:
        """Run all 5 implementations and return results."""
        return [self.search(target, arr, algo) for algo in SearchAlgorithm]


# =============================================================================
# Commands (Write Model - CQRS)
# =============================================================================

@dataclass
class RecordSearchCommand:
    target: int
    array: list[int]
    algorithm: SearchAlgorithm


class SearchCommandHandler:
    """Command handler for recording searches."""

    def __init__(self, service: BinarySearchService):
        self._service = service

    def handle_record_search(self, cmd: RecordSearchCommand) -> SearchResult:
        return self._service.search(cmd.target, cmd.array, cmd.algorithm)


# =============================================================================
# Queries (Read Model - CQRS)
# =============================================================================

@dataclass
class SearchQuery:
    target: int
    array: list[int]
    algorithm: SearchAlgorithm | None = None


@dataclass
class SearchQueryResult:
    results: list[SearchResult]
    history: list[SearchResult]
    stats: dict


class SearchQueryHandler:
    """Query handler for search operations."""

    def __init__(self, service: BinarySearchService, history_repo: SearchHistoryRepository):
        self._service = service
        self._history_repo = history_repo

    def handle_search(self, query: SearchQuery) -> SearchQueryResult:
        if query.algorithm:
            results = [self._service.search(query.target, query.array, query.algorithm)]
        else:
            results = self._service.search_all(query.target, query.array)

        history = self._history_repo.get_history(query.algorithm)
        stats = self._history_repo.get_stats(query.algorithm)

        return SearchQueryResult(
            results=results,
            history=history,
            stats=stats
        )


# =============================================================================
# Facade / Application Service
# =============================================================================

class KarateChop:
    """Main facade for the karate chop (binary search) system."""

    def __init__(self):
        self._history_repo = InMemorySearchHistoryRepository()
        self._service = BinarySearchService(self._history_repo)
        self._command_handler = SearchCommandHandler(self._service)
        self._query_handler = SearchQueryHandler(self._service, self._history_repo)

    # Commands
    def record_search(
        self, target: int, array: list[int], algorithm: SearchAlgorithm
    ) -> SearchResult:
        cmd = RecordSearchCommand(target=target, array=array, algorithm=algorithm)
        return self._command_handler.handle_record_search(cmd)

    # Queries
    def search(
        self, target: int, array: list[int], algorithm: SearchAlgorithm | None = None
    ) -> SearchQueryResult:
        query = SearchQuery(target=target, array=array, algorithm=algorithm)
        return self._query_handler.handle_search(query)

    def search_one(self, target: int, array: list[int], algorithm: SearchAlgorithm) -> SearchResult:
        return self._service.search(target, array, algorithm)

    def search_all(self, target: int, array: list[int]) -> list[SearchResult]:
        return self._service.search_all(target, array)

    def get_history(self, algorithm: SearchAlgorithm | None = None) -> list[SearchResult]:
        return self._history_repo.get_history(algorithm)

    def get_stats(self, algorithm: SearchAlgorithm | None = None) -> dict:
        return self._history_repo.get_stats(algorithm)


# =============================================================================
# Convenience Functions (Functional Alternative)
# =============================================================================

def chop(target: int, arr: list[int]) -> int:
    """Simple functional interface - returns index or -1.
    
    Uses iterative implementation as default.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def chop_iterative(target: int, arr: list[int]) -> int:
    """Iterative implementation."""
    return chop(target, arr)


def chop_recursive(target: int, arr: list[int]) -> int:
    """Recursive implementation."""
    def _rec(low: int, high: int) -> int:
        if low > high:
            return -1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return _rec(mid + 1, high)
        else:
            return _rec(low, mid - 1)
    return _rec(0, len(arr) - 1)


def chop_functional(target: int, arr: list[int]) -> int:
    """Functional with slices."""
    def _func(sub_arr: list[int], offset: int) -> int:
        if not sub_arr:
            return -1
        mid = len(sub_arr) // 2
        if sub_arr[mid] == target:
            return offset + mid
        elif sub_arr[mid] < target:
            return _func(sub_arr[mid + 1:], offset + mid + 1)
        else:
            return _func(sub_arr[:mid], offset)
    return _func(arr, 0)


def chop_builtin(target: int, arr: list[int]) -> int:
    """Using bisect."""
    index = bisect_left(arr, target)
    return index if index < len(arr) and arr[index] == target else -1


def chop_tail_recursive(target: int, arr: list[int]) -> int:
    """Tail-recursive implementation."""
    def _tail(low: int, high: int) -> int:
        if low > high:
            return -1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return _tail(mid + 1, high)
        else:
            return _tail(low, mid - 1)
    return _tail(0, len(arr) - 1)


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    # Test array
    arr = [1, 3, 5, 7, 9, 11, 13, 15]

    print("=== Karate Chop - 5 Implementations ===\n")
    print(f"Array: {arr}\n")

    # Test cases from kata
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
    ]

    algorithms = [
        ("Iterative", chop_iterative),
        ("Recursive", chop_recursive),
        ("Functional", chop_functional),
        ("Built-in (bisect)", chop_builtin),
        ("Tail-Recursive", chop_tail_recursive),
    ]

    for target, test_arr in test_cases:
        print(f"chop({target}, {test_arr}) =>")
        for name, func in algorithms:
            result = func(target, test_arr)
            print(f"  {name:20s}: {result}")
        print()

    # Using the full facade
    print("=== Using KarateChop Facade ===")
    kc = KarateChop()
    result = kc.search_all(3, [1, 3, 5])
    for r in result:
        print(
            f"  {r.algorithm.value:15s}: index={r.index:2d}, "
            f"iterations={r.iterations}, comparisons={r.comparisons}"
        )

    print(f"\nStats: {kc.get_stats()}")