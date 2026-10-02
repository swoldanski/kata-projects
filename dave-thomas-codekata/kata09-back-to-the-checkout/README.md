# Kata09: Back to the Checkout

Source: http://codekata.com/kata/kata09-back-to-the-checkout/

## Problem

Revisit the supermarket pricing problem (Kata01) but now implement a working checkout system that calculates the total price for a basket of items.

## Goals

- Implement pricing rules from Kata01:
  - Simple prices (per item)
  - Volume discounts (3 for $1)
  - Weight-based ($1.99/lb)
  - Buy N get M free
- Handle scanning items in any order
- Produce itemized receipt
- Support adding/removing items

## Examples

```python
# Basic usage
checkout = Checkout()
checkout.add_item("apple", 1.00)
checkout.add_item("apple", 1.00)
checkout.add_item("apple", 1.00)  # 3 for $1
checkout.total()  # => 1.00 (volume discount applied)

# Weight-based
checkout.add_item("bananas", weight_lbs=2.5)  # $1.99/lb
checkout.total()  # => 1.00 + 4.975 = 5.975

# Buy N get M free
checkout.add_item("orange", 0.50)
checkout.add_item("orange", 0.50)  # Buy 2 get 1 free
checkout.add_item("orange", 0.50)  # Free!
checkout.total()  # => 5.975 + 1.00 = 6.975
```

## Exercises

1. Basic checkout with simple prices
2. Add volume pricing (tiered pricing)
3. Add weight-based items
4. Add "buy N get M free" promotions
5. Receipt formatting (item, qty, unit price, total)
6. Remove items (void last, void specific)
7. Persistent pricing rules (load from config)
8. Tax calculation
9. Loyalty discounts