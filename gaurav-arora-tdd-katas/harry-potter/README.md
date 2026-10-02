# Harry Potter Kata

Source: https://github.com/garora/TDD-Katas#harry-potter-

## Problem

Calculate the price of a basket of Harry Potter books with discounts for buying different books.

## Pricing

- 1 book: €8.00
- 2 different: 5% discount
- 3 different: 10% discount
- 4 different: 20% discount
- 5 different: 25% discount

## Examples

```
2 copies of Book 1: 2 × 8 = €16.00
Book 1 + Book 2: 2 × 8 × 0.95 = €15.20
Book 1 + Book 2 + Book 3: 3 × 8 × 0.90 = €21.60
Book 1 + Book 2 + Book 3 + Book 4: 4 × 8 × 0.80 = €25.60
All 5: 5 × 8 × 0.75 = €30.00
```

## Complex Case

```
Book 1 × 2, Book 2 × 2, Book 3 × 2, Book 4 × 1, Book 5 × 1
Optimal: (5 different) + (3 different) = 30.00 + 21.60 = €51.60
Not: (4 different) + (4 different) = 25.60 + 25.60 = €51.20
```

## TDD Steps

1. Single book
2. Two same books
3. Two different books
4. Three different
5. Four different
6. Five different
7. Multiple copies (optimization needed)