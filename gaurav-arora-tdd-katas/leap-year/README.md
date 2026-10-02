# Leap Year Kata

Source: https://github.com/garora/TDD-Katas#leap-year-

## Problem

Determine if a given year is a leap year.

## Rules (Gregorian Calendar)

1. Divisible by 4 → leap year
2. Except divisible by 100 → not leap year
3. Except divisible by 400 → leap year

## Examples

```
1996 → true  (div by 4)
1900 → false (div by 100, not 400)
2000 → true  (div by 400)
2001 → false
```

## TDD Steps

1. 2001 → false
2. 1996 → true
3. 1900 → false
4. 2000 → true
5. Edge cases: year 0, negative