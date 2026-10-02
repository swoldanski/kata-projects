"""oddeven-kata - OddEven - Partition numbers

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


class OddEven:
    """Return (odds, evens)"""

    def __init__(self):
        raise NotImplementedError("Implement OddEven")

    def partition_oddeven(self, numbers: list[int]) -> tuple:
        """Return (odds, evens)"""
        raise NotImplementedError("Implement partition_oddeven")


# Functional alternative (for simpler katas)
def partition_oddeven(numbers: list[int]) -> tuple:
    """Return (odds, evens)"""
    raise NotImplementedError("Implement partition_oddeven")
