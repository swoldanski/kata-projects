# Mine Fields Kata

Source: https://github.com/garora/TDD-Katas#mine-fields-

## Problem

Generate a Minesweeper field with numbers indicating adjacent mines.

## Input

- Width, height
- Number of mines (or mine positions)

## Output

Grid where:
- `*` = mine
- `0-8` = count of adjacent mines (including diagonals)

## Example

```
Input: 3x3, mine at (1,1) [center]
Output:
111
1*1
111
```

## Requirements

1. Generate random mine placement
2. Calculate numbers for all non-mine cells
3. Handle edges/corners correctly
4. Support custom mine positions for testing

## TDD Steps

1. Empty field (no mines) → all 0
2. Single mine in center
3. Mine in corner
4. Mine on edge
5. Multiple mines
6. Full field (all mines)