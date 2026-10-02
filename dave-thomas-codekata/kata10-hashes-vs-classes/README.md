# Kata10: Hashes vs. Classes

Source: http://codekata.com/kata/kata10-hashes-vs-classes/

## Problem

Explore the tradeoff between using hashes/dictionaries (data-only) vs. classes (data + behavior) to represent domain objects.

## Goals

- Implement the same domain model both ways
- Compare:
  - Code organization
  - Encapsulation
  - Extensibility
  - Testability
  - Performance
  - Serialization

## Examples

```python
# Hash-based approach
Order = dict  # {id, customer_id, items: [{product, qty, price}], status}
def calculate_total(order: dict) -> float:
    return sum(item["qty"] * item["price"] for item in order["items"])

# Class-based approach
class Order:
    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.items: List[LineItem] = []
        self.status = "pending"
    
    def add_item(self, product: str, qty: int, price: float):
        self.items.append(LineItem(product, qty, price))
    
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)
```

## Exercises

1. Model a simple domain (e.g., Order with LineItems, Customer, Payment)
2. Hash-based: plain dicts/DataClasses/structs with separate functions
3. Class-based: methods on objects, encapsulation, invariants
4. Add a new requirement (e.g., discounts, shipping, tax)
5. Refactor each approach
6. Compare LOC, coupling, ease of change
7. Try with functional core / imperative shell