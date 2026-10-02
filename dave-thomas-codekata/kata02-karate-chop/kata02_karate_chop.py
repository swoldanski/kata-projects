"""kata02-karate-chop - Karate Chop - Binary search with 5 implementations

Source: See README.md
"""

from typing import List, Optional, Dict, Any, Tuple, Set


# TODO: Implement the kata here
# Follow DDD, CQRS, Repository patterns with in-memory state
# No database, no ORM, no external persistence
# Use domain entities, value objects, aggregates, domain services
# Separate commands (writes) from queries (reads)
# Abstract data access behind repository interfaces
# Use in-memory collections (lists, dicts, sets) for state


class KarateChop:
    """Return index of target in sorted array, or -1"""
    
    def __init__(self):
        raise NotImplementedError("Implement KarateChop")
    
    def chop(self, target: int, arr: List[int]) -> int:
        """Return index of target in sorted array, or -1"""
        raise NotImplementedError("Implement chop")


# Functional alternative (for simpler katas)
def chop(target: int, arr: List[int]) -> int:
    """Return index of target in sorted array, or -1"""
    raise NotImplementedError("Implement chop")
