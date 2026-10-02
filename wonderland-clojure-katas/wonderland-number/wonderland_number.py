"""wonderland-number - Wonderland Number - Number sequences

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


class WonderlandNumber:
    """Generate number sequence"""
    
    def __init__(self):
        raise NotImplementedError("Implement WonderlandNumber")
    
    def generate_sequence(self, name: str, n: int) -> List[int]:
        """Generate number sequence"""
        raise NotImplementedError("Implement generate_sequence")


# Functional alternative (for simpler katas)
def generate_sequence(name: str, n: int) -> List[int]:
    """Generate number sequence"""
    raise NotImplementedError("Implement generate_sequence")
