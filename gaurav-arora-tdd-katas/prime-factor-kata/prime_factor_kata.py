"""prime-factor-kata - Prime Factors - Prime factorization

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


class PrimeFactor:
    """Return prime factors of n"""

    def __init__(self):
        raise NotImplementedError("Implement PrimeFactor")

    def prime_factors(self, n: int) -> list[int]:
        """Return prime factors of n"""
        raise NotImplementedError("Implement prime_factors")


# Functional alternative (for simpler katas)
def prime_factors(n: int) -> list[int]:
    """Return prime factors of n"""
    raise NotImplementedError("Implement prime_factors")
