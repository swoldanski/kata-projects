"""kata09-back-to-the-checkout - Back to the Checkout - Supermarket checkout

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


class BackToCheckout:
    """Checkout system with pricing rules"""

    def __init__(self):
        raise NotImplementedError("Implement BackToCheckout")



# Functional alternative (for simpler katas)
def Checkout() -> None:
    """Checkout system with pricing rules"""
    raise NotImplementedError("Implement Checkout")
