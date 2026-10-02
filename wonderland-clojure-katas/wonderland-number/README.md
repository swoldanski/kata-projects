# Wonderland Number

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/wonderland-number

## Problem

Explore number sequences and properties inspired by Alice in Wonderland. Mathematical recreation.

## Possible Directions

1. **Look-and-say sequence** (Conway's constant)
2. **Collatz conjecture** sequences
3. **Fibonacci** and Lucas numbers
4. **Prime number** patterns
5. **Happy numbers**
6. **Kaprekar's routine** (6174)
7. **Palindromic numbers**
8. **Digital roots**

## Goals

- Generate sequences
- Find patterns
- Visualize
- Test conjectures computationally

## Examples

```python
# Number sequences
generate_sequence("collatz", 10)      # => [10, 5, 16, 8, 4, 2, 1]
generate_sequence("fibonacci", 10)    # => [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
generate_sequence("look_and_say", 5)  # => ["1", "11", "21", "1211", "111221"]
```

## Exercises

1. Implement 5+ sequences
2. Find first N terms
3. Detect cycles
4. Statistical analysis
5. Visualize as graphs/spirals
6. Parallel computation for large terms