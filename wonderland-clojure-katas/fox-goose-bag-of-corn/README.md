# Fox, Goose, Bag of Corn

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/fox-goose-bag-of-corn

## Problem

Classic river crossing puzzle: A farmer must transport a fox, a goose, and a bag of corn across a river using a boat that holds only the farmer plus one item.

## Constraints

- Fox eats goose if left alone
- Goose eats corn if left alone
- Farmer must be present to prevent eating
- Boat holds farmer + 1 item

## Goal

Find the sequence of moves to get all safely across.

## State Representation

- Each entity: {Farmer, Fox, Goose, Corn} × {Left, Right}
- Valid states: no eating when farmer absent
- Transitions: farmer crosses with 0 or 1 item

## Examples

```python
# River crossing solution
solution = solve_river_crossing()
# => [
#   "Farmer takes Goose across",
#   "Farmer returns alone",
#   "Farmer takes Fox across",
#   "Farmer returns with Goose",
#   "Farmer takes Corn across",
#   "Farmer returns alone",
#   "Farmer takes Goose across"
# ]
```

## Exercises

1. Model state and valid transitions
2. BFS/DFS to find solution
3. Visualize solution steps
4. Generalize: N items, M constraints
5. Find all solutions
6. Minimal moves
7. Interactive solver