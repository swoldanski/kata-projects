"""kata19-word-chains - Word Chains - Word ladder

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


class WordChains:
    """Find shortest word chain"""
    
    def __init__(self):
        raise NotImplementedError("Implement WordChains")
    
    def word_chain(self, start: str, end: str, dictionary: List[str]) -> List[str]:
        """Find shortest word chain"""
        raise NotImplementedError("Implement word_chain")


# Functional alternative (for simpler katas)
def word_chain(start: str, end: str, dictionary: List[str]) -> List[str]:
    """Find shortest word chain"""
    raise NotImplementedError("Implement word_chain")
