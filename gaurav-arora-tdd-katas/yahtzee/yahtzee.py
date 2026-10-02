"""yahtzee - Yahtzee - Dice game scoring

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


class Yahtzee:
    """Score Yahtzee category"""
    
    def __init__(self):
        raise NotImplementedError("Implement Yahtzee")
    
    def score_category(self, category: str, dice: List[int]) -> int:
        """Score Yahtzee category"""
        raise NotImplementedError("Implement score_category")


# Functional alternative (for simpler katas)
def score_category(category: str, dice: List[int]) -> int:
    """Score Yahtzee category"""
    raise NotImplementedError("Implement score_category")
