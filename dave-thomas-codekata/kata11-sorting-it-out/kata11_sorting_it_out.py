"""kata11-sorting-it-out - Sorting It Out - Multiple sorting algorithms

Source: See README.md
"""



from typing import Any  # noqa: F401  (generated stub shape)

# TODO: Implement the kata here
# Follow DDD, CQRS, Repository patterns with in-memory state
# No database, no ORM, no external persistence
# Use domain entities, value objects, aggregates, domain services
# Separate commands (writes) from queries (reads)
# Abstract data access behind repository interfaces
# Use in-memory collections (lists, dicts, sets) for state


class SortingItOut:
    """Sort using specified algorithm"""

    def __init__(self):
        raise NotImplementedError("Implement SortingItOut")

    def sort(self, arr: list[int], algorithm: str) -> list[int]:
        """Sort using specified algorithm"""
        raise NotImplementedError("Implement sort")


# Functional alternative (for simpler katas)
def sort(arr: list[int], algorithm: str) -> list[int]:
    """Sort using specified algorithm"""
    raise NotImplementedError("Implement sort")
