"""harry-potter - Harry Potter - Book discount pricing

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


class HarryPotter:
    """Calculate price with discounts"""

    def __init__(self):
        raise NotImplementedError("Implement HarryPotter")

    def calculate_price(self, books: list[int]) -> float:
        """Calculate price with discounts"""
        raise NotImplementedError("Implement calculate_price")


# Functional alternative (for simpler katas)
def calculate_price(books: list[int]) -> float:
    """Calculate price with discounts"""
    raise NotImplementedError("Implement calculate_price")
