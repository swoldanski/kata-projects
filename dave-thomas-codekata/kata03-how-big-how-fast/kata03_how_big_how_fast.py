"""kata03-how-big-how-fast - How Big? How Fast? - Estimation exercises

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


class HowBigHowFast:
    """Estimate bits needed for unsigned representation of n"""
    
    def __init__(self):
        raise NotImplementedError("Implement HowBigHowFast")
    
    def estimate_bits(self, n: int) -> int:
        """Estimate bits needed for unsigned representation of n"""
        raise NotImplementedError("Implement estimate_bits")


# Functional alternative (for simpler katas)
def estimate_bits(n: int) -> int:
    """Estimate bits needed for unsigned representation of n"""
    raise NotImplementedError("Implement estimate_bits")
