"""recently-used-list - Recently Used List - LRU cache

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


class RecentlyUsedList:
    """LRU-style recently used list"""

    def __init__(self):
        raise NotImplementedError("Implement RecentlyUsedList")

    def RecentlyUsedList(self, capacity: int) -> None:
        """LRU-style recently used list"""
        raise NotImplementedError("Implement RecentlyUsedList")
