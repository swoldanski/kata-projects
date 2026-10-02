# Game of Life

Source: https://github.com/garora/TDD-Katas#game-of-life-

## Problem

Implement Conway's Game of Life — a cellular automaton.

## Rules

Grid of cells, each alive or dead. Next generation:
1. Live cell with < 2 neighbors → dies (underpopulation)
2. Live cell with 2-3 neighbors → lives
3. Live cell with > 3 neighbors → dies (overpopulation)
4. Dead cell with exactly 3 neighbors → becomes alive (reproduction)

## Requirements

1. Infinite grid (or large finite with wrapping)
2. `next_generation(grid)` → new grid
3. Support patterns: blinker, glider, gun
4. Multiple generations

## Examples

```python
# Game of Life
gol = GameOfLife()
gol.add_live_cell(1, 0)
gol.add_live_cell(1, 1)
gol.add_live_cell(1, 2)  # Blinker pattern

gol.next_generation()
# Blinker oscillates: vertical <-> horizontal
```

## TDD Steps

1. Dead cell stays dead
2. Live cell with 0 neighbors dies
3. Live cell with 1 neighbor dies
4. Live cell with 2 neighbors lives
5. Live cell with 3 neighbors lives
6. Live cell with 4 neighbors dies
7. Dead cell with 3 neighbors becomes alive
8. Blinker oscillates
9. Glider moves

## Representations

- Set of live coordinates (infinite grid)
- 2D array (finite grid)
- Sparse matrix