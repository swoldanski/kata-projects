# Poker Hands Kata

Source: https://github.com/garora/TDD-Katas#poker-hands

## Problem

Compare two poker hands and determine the winner.

## Hand Rankings (high to low)

1. **Royal Flush**: A,K,Q,J,10 same suit
2. **Straight Flush**: 5 consecutive same suit
3. **Four of a Kind**: 4 same rank
4. **Full House**: 3 + 2 same rank
5. **Flush**: 5 same suit
6. **Straight**: 5 consecutive rank
7. **Three of a Kind**: 3 same rank
8. **Two Pair**: 2 pairs
9. **One Pair**: 1 pair
10. **High Card**: highest card

## Tie Breaking

- Higher rank wins
- For same rank: compare kickers
- For straights: highest card wins (A can be low: A,2,3,4,5)

## Requirements

1. Parse hand string: "2H 3D 5S 9C KD"
2. Rank hand
3. Compare two hands → "Player 1 wins", "Player 2 wins", "Tie"

## Examples

```python
# Hand comparison
compare_hands("2H 3D 5S 9C KD", "2C 3H 4S 8C AH")  # => "Player 2 wins" (high card Ace)
compare_hands("2H 2D 5S 9C KD", "2C 3H 4S 8C AH")  # => "Player 1 wins" (pair vs high card)
compare_hands("2H 2D 4C 4D 4S", "3H 3D 3S 9C 9D")  # => "Player 2 wins" (full house)
```

## TDD Steps

1. High card vs high card
2. One pair vs high card
3. Two pair vs one pair
4. Three of a kind
5. Straight
6. Flush
7. Full house
8. Four of a kind
9. Straight flush
10. Royal flush
11. Tie breakers