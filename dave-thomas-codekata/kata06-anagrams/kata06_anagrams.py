"""kata06-anagrams - Anagrams - Group words by anagram

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


class Anagrams:
    """Group words into anagram sets"""
    
    def __init__(self):
        raise NotImplementedError("Implement Anagrams")
    
    def group_anagrams(self, words: List[str]) -> List[List[str]]:
        """Group words into anagram sets"""
        raise NotImplementedError("Implement group_anagrams")


# Functional alternative (for simpler katas)
def group_anagrams(words: List[str]) -> List[List[str]]:
    """Group words into anagram sets"""
    raise NotImplementedError("Implement group_anagrams")
