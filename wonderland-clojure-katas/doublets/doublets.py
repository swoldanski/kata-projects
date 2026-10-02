"""doublets - Doublets - Word ladders

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


class Doublets:
    """Find word ladder"""

    def __init__(self):
        raise NotImplementedError("Implement Doublets")

    def find_doublet_chain(self, start: str, end: str, dictionary: list[str]) -> list[str]:
        """Find word ladder"""
        raise NotImplementedError("Implement find_doublet_chain")


# Functional alternative (for simpler katas)
def find_doublet_chain(start: str, end: str, dictionary: list[str]) -> list[str]:
    """Find word ladder"""
    raise NotImplementedError("Implement find_doublet_chain")
