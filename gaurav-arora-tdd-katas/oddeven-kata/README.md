# OddEven Kata

Source: https://github.com/garora/TDD-Katas#the-oddeven-kata

## Problem

Given a list of integers, separate them into odd and even numbers.

## Requirements

1. `odds(list)` → list of odd numbers
2. `evens(list)` → list of even numbers
3. Handle empty list
4. Handle negative numbers
5. Preserve order
6. Single pass (optional optimization)

## Examples

```python
partition_oddeven([])              # => ([], [])
partition_oddeven([1])             # => ([1], [])
partition_oddeven([2])             # => ([], [2])
partition_oddeven([1, 2, 3, 4])    # => ([1, 3], [2, 4])
partition_oddeven([-1, -2, 0])     # => ([-1], [-2, 0])
```

## TDD Steps

1. Empty list → [], []
2. Single odd → [n], []
3. Single even → [], [n]
4. Mixed → odds, evens
5. Negatives
6. Large list

## Extensions

- Partition into N groups (mod N)
- Stream processing (lazy)
- Parallel partition