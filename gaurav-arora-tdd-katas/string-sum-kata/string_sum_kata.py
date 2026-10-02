"""string-sum-kata - String Sum - Sum numbers in string

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


class StringSum:
    """Sum comma-separated numbers"""

    def __init__(self):
        raise NotImplementedError("Implement StringSum")

    def string_sum(self, s: str) -> int:
        """Sum comma-separated numbers"""
        raise NotImplementedError("Implement string_sum")


# Functional alternative (for simpler katas)
def string_sum(s: str) -> int:
    """Sum comma-separated numbers"""
    raise NotImplementedError("Implement string_sum")
