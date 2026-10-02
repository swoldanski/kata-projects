"""kata07-howd-i-do - How'd I Do? - Quiz scoring system

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


class HowdIDo:
    """Calculate quiz score"""
    
    def __init__(self):
        raise NotImplementedError("Implement HowdIDo")
    
    def score_quiz(self, answers: List[str], key: List[str]) -> int:
        """Calculate quiz score"""
        raise NotImplementedError("Implement score_quiz")


# Functional alternative (for simpler katas)
def score_quiz(answers: List[str], key: List[str]) -> int:
    """Calculate quiz score"""
    raise NotImplementedError("Implement score_quiz")
