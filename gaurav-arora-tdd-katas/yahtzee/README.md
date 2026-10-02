# Yahtzee Kata

Source: https://github.com/garora/TDD-Katas#yahtzee-

## Problem

Score a Yahtzee dice game.

## Categories (score card)

**Upper Section** (sum of matching dice):
- Ones, Twos, Threes, Fours, Fives, Sixes
- Bonus: 35 if upper ≥ 63

**Lower Section**:
- **3 of a Kind**: sum all dice
- **4 of a Kind**: sum all dice
- **Full House**: 25 (3+2)
- **Small Straight**: 30 (4 consecutive)
- **Large Straight**: 40 (5 consecutive)
- **Yahtzee**: 50 (5 of a kind)
- **Chance**: sum all dice

## Requirements

1. `score(category, dice[5])` → points
2. Validate dice (5 values, 1-6)
3. Upper section bonus
4. Total score

## Examples

```python
score("ones", [1, 1, 1, 4, 5])        # => 3
score("full_house", [2, 2, 3, 3, 3])  # => 25
score("yahtzee", [4, 4, 4, 4, 4])     # => 50
score("chance", [1, 2, 3, 4, 5])      # => 15
```

## TDD Steps

1. Upper section: ones through sixes
2. 3 of a kind
3. 4 of a kind
4. Full house
5. Small straight
6. Large straight
7. Yahtzee
8. Chance
9. Upper bonus
10. Full game scoring