"""poker-hands - Poker Hands - Hand ranking

Source: See README.md
"""



from typing import Any  # noqa: F401  (generated stub shape)

# TODO: Implement the kata here
# Follow DDD, CQRS, Repository patterns with in-memory state
# No database, no ORM, no external persistence
# Use domain entities, value objects, aggregates, domain services
# Separate commands (writes) from queries (reads)
# Abstract data access behind repository interfaces
# Use in-memory collections (lists, dicts, sets) for state


class PokerHands:
    """Compare two poker hands"""

    def __init__(self):
        raise NotImplementedError("Implement PokerHands")

    def compare_hands(self, hand1: str, hand2: str) -> str:
        """Compare two poker hands"""
        raise NotImplementedError("Implement compare_hands")


# Functional alternative (for simpler katas)
def compare_hands(hand1: str, hand2: str) -> str:
    """Compare two poker hands"""
    raise NotImplementedError("Implement compare_hands")
