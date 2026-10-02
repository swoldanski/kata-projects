# Prime Factor Kata (via Uncle Bob)

Source: https://github.com/garora/TDD-Katas#the-primefactor-kata-via-uncle-bob

## Problem

Compute the prime factors of a given integer.

## Requirements

1. `prime_factors(n)` → list of prime factors in ascending order
2. Product of factors = n
3. Handle n ≤ 1 (empty list or error)

## Examples

```
1   → []
2   → [2]
3   → [3]
4   → [2, 2]
6   → [2, 3]
8   → [2, 2, 2]
9   → [3, 3]
12  → [2, 2, 3]
999 → [3, 3, 3, 37]
```

## TDD Steps

1. 1 → []
2. 2 → [2]
3. 3 → [3]
4. 4 → [2, 2]
5. 6 → [2, 3]
6. 8 → [2, 2, 2]
7. 9 → [3, 3]
8. Large prime
9. Large composite

## Algorithm

Trial division up to √n, then remaining n if > 1.