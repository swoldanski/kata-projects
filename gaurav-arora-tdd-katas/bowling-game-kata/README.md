# The Bowling Game Kata (via Uncle Bob)

Source: https://github.com/garora/TDD-Katas#the-bowling-game-kata-via-uncle-bob

## Problem

Score a game of ten-pin bowling.

## Rules

- 10 frames
- Each frame: up to 2 rolls to knock down 10 pins
- **Strike**: 10 pins on first roll → frame ends, score = 10 + next 2 rolls
- **Spare**: 10 pins in 2 rolls → score = 10 + next roll
- **Open frame**: < 10 pins → score = pins knocked down
- **10th frame**: bonus rolls for strike/spare (max 3 rolls)

## Scoring Examples

```
X X X X X X X X X X X X  (12 strikes) = 300
9- 9- 9- 9- 9- 9- 9- 9- 9- 9-  (9 + miss each frame) = 90
5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/5  (all 5/ spare) = 150
```

## TDD Steps

1. Gutter game (all 0) → 0
2. All ones → 20
3. One spare → 10 + next roll
4. One strike → 10 + next 2 rolls
5. Perfect game → 300

## Design

- `roll(pins)` method
- `score()` method
- Internal: array of rolls, calculate on demand