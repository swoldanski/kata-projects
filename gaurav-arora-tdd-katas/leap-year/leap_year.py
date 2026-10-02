"""leap-year - Leap Year - Gregorian calendar

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


class LeapYear:
    """Check if leap year"""
    
    def __init__(self):
        raise NotImplementedError("Implement LeapYear")
    
    def is_leap_year(self, year: int) -> bool:
        """Check if leap year"""
        raise NotImplementedError("Implement is_leap_year")


# Functional alternative (for simpler katas)
def is_leap_year(year: int) -> bool:
    """Check if leap year"""
    raise NotImplementedError("Implement is_leap_year")
