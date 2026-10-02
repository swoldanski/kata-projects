# Magic Square

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/magic-square

## Problem

Generate magic squares: N×N grids filled with distinct positive integers where each row, column, and diagonal sums to the same magic constant.

## Properties

- Order N: uses numbers 1 to N²
- Magic constant: M = N(N²+1)/2
- Example N=3: M = 15

```
8 1 6
3 5 7
4 9 2
```

## Goals

- Generate magic squares for odd N (Siamese method)
- Generate for doubly-even N (4, 8, 12...)
- Generate for singly-even N (6, 10, 14...)
- Verify magic square properties

## Algorithms

1. **Siamese (De la Loubère)** — odd N
2. **Doubly-even** — pattern-based
3. **Singly-even (Strachey)** — composite method
4. **Backtracking** — general but slow

## Exercises

1. Siamese method for odd N
2. Doubly-even pattern
3. Strachey method for singly-even
4. Verify any square
5. Count distinct squares (symmetries)
6. Magic cubes (3D)
7. Prime magic squares