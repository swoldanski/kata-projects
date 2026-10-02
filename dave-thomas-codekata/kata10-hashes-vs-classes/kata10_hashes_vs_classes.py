"""kata10-hashes-vs-classes - Hashes vs Classes - Data vs behavior

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


class HashesVsClasses:
    """Order as class vs hash comparison"""
    
    def __init__(self):
        raise NotImplementedError("Implement HashesVsClasses")
    
    def Order(self, ) -> None:
        """Order as class vs hash comparison"""
        raise NotImplementedError("Implement Order")


# Functional alternative (for simpler katas)
def Order() -> None:
    """Order as class vs hash comparison"""
    raise NotImplementedError("Implement Order")
