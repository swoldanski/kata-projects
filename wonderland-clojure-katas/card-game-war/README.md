# Card Game War

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/card-game-war

## Problem

Simulate the card game "War" between two players.

## Rules

1. Standard 52-card deck, split evenly (26 each)
2. Each player reveals top card
3. Higher card wins, takes both cards (winner's card on top)
4. If tie: "War" — each plays 3 face down, 1 face up, compare face-up
5. Winner takes all cards in the war
6. Game ends when one player has all 52 cards

## Goals

- Model deck, cards, players
- Implement game logic
- Handle war scenarios
- Detect infinite games (cycle detection)
- Statistics: turns, wars, max cards held

## Examples

```python
# War simulation
result = play_war()
# => {"winner": "Player 1", "turns": 1247, "wars": 23, "max_cards": 45}
```

## Exercises

1. Basic simulation (no war)
2. Full war implementation
3. Cycle detection (game can loop infinitely)
4. Multiple games statistics
5. Variations: 3+ players, different deck sizes
6. Visualization of game state