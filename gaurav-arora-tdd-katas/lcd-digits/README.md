# LCD Digits Kata

Source: https://github.com/garora/TDD-Katas#lcd-digits-

## Problem

Display numbers in LCD/7-segment style using ASCII characters.

## Format

Each digit is 3 columns wide, 3 rows tall:
```
 -       -   -       -   -   -   -   -   -
| |   |   |   | | | |   |     | | | | | |
 -   -   -   -   -       -   -   -   -
| |   | |     |   |   | | |   | | |   |
 -       -   -       -   -       -   -
```

## Requirements

1. `lcd(number, size=1)` → string with line breaks
2. Size parameter scales horizontally and vertically
3. Handle multi-digit numbers
4. Handle negative sign (optional)

## Example (size=1)

```
    -   -
  | |_  _|
  | _|  _|
```

## TDD Steps

1. Single digit "0"
2. Single digit "1"
3. All digits 0-9
4. Multi-digit "123"
5. Size 2
6. Size 3
7. Negative numbers