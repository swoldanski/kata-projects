# Kata12: Best Sellers

Source: http://codekata.com/kata/kata12-best-sellers/

## Problem

Given a stream of sales transactions, maintain a real-time "top N best sellers" list.

## Requirements

- Implement a `TopK` class/function that maintains the top K items from a stream
- `add(item, score)` — add/update item with score
- `top(k)` — return top k items (descending by score)
- Handle ties consistently (e.g., by item name, insertion order)
- Support time-based expiration (sliding window)
- Efficient: O(log k) per insertion, O(k) for top-k query

## Goals

- Efficient streaming algorithm for top-K
- Handle high throughput
- Deal with ties
- Support time windows (last hour, day, week)

## Approaches

1. **Full sort** — O(n log n) each query
2. **Min-heap of size K** — O(n log k) insert, O(k) to extract
3. **Count-Min Sketch** — approximate, O(1) space per item
4. **Lossy counting** — approximate frequent items
5. **Space-Saving algorithm** — exact top-k with bounded memory

## Examples

```python
# Basic usage
topk = TopK(3)
topk.add("apple", 10)
topk.add("banana", 5)
topk.add("cherry", 15)
topk.add("date", 8)
topk.top(3)  # => [("cherry", 15), ("apple", 10), ("date", 8)]

# With ties
topk.add("elderberry", 10)  # same score as apple
topk.top(3)  # => consistent tie-breaking
```

## Exercises

1. Basic top-K with heap
2. Handle ties (alphabetical? first seen?)
3. Sliding time window (expire old sales)
4. Multiple categories (top per category)
5. Approximate algorithms for massive streams
6. Persistence and recovery
7. Dashboard API