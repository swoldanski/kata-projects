"""alphabet-cipher - Alphabet Cipher - Substitution cipher

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


class AlphabetCipher:
    """Substitution cipher with keyword"""
    
    def __init__(self):
        raise NotImplementedError("Implement AlphabetCipher")
    
    def AlphabetCipher(self, keyword: str) -> None:
        """Substitution cipher with keyword"""
        raise NotImplementedError("Implement AlphabetCipher")


# Functional alternative (for simpler katas)
def AlphabetCipher(keyword: str) -> None:
    """Substitution cipher with keyword"""
    raise NotImplementedError("Implement AlphabetCipher")
