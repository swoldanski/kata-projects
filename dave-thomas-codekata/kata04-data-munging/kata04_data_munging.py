"""kata04-data-munging - Data Munging - Weather and soccer data parsing

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


class DataMunging:
    """Return day with smallest temperature spread"""
    
    def __init__(self):
        raise NotImplementedError("Implement DataMunging")
    
    def find_min_spread_day(self, weather_data: str) -> int:
        """Return day with smallest temperature spread"""
        raise NotImplementedError("Implement find_min_spread_day")


# Functional alternative (for simpler katas)
def find_min_spread_day(weather_data: str) -> int:
    """Return day with smallest temperature spread"""
    raise NotImplementedError("Implement find_min_spread_day")
