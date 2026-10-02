"""kata12-best-sellers - Best Sellers - Top-K streaming

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


class BestSellers:
    """Maintain top K items from stream"""
    
    def __init__(self):
        raise NotImplementedError("Implement BestSellers")
    
    def TopK(self, ) -> None:
        """Maintain top K items from stream"""
        raise NotImplementedError("Implement TopK")


# Functional alternative (for simpler katas)
def TopK() -> None:
    """Maintain top K items from stream"""
    raise NotImplementedError("Implement TopK")
