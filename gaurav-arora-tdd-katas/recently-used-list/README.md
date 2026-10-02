# Recently Used List Kata

Source: https://github.com/garora/TDD-Katas#recently-used-list-

## Problem

Implement a "recently used" list (LRU cache style) with a maximum capacity.

## Requirements

1. `add(item)` — add to front, remove if already exists
2. `get(index)` — return item at index (0 = most recent)
3. `size()` — current count
4. `capacity()` — max capacity
5. When capacity exceeded, remove least recently used
6. No duplicates (move to front on re-add)

## Example

```
capacity = 3
add("a") → [a]
add("b") → [b, a]
add("c") → [c, b, a]
add("d") → [d, c, b]  (a removed)
add("b") → [b, d, c]  (b moved to front)
```

## TDD Steps

1. Add single item
2. Add multiple, check order
3. Capacity limit
4. Duplicate moves to front
5. Get by index
6. Edge cases: empty, invalid index