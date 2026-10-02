"""kata13-counting-code-lines - Counting Code Lines - LOC counter

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


class CountingCodeLines:
    """Count code/comment/blank lines"""
    
    def __init__(self):
        raise NotImplementedError("Implement CountingCodeLines")
    
    def count_lines(self, path: str) -> dict:
        """Count code/comment/blank lines"""
        raise NotImplementedError("Implement count_lines")


# Functional alternative (for simpler katas)
def count_lines(path: str) -> dict:
    """Count code/comment/blank lines"""
    raise NotImplementedError("Implement count_lines")
