# Reversi (Othello) Kata

Source: https://github.com/garora/TDD-Katas#reversi-

## Problem

Implement the game logic for Reversi/Othello.

## Rules

- 8×8 board, 4 initial pieces (2 each, diagonal)
- Players alternate placing pieces
- Must capture at least one opponent piece
- Capture: bracket opponent pieces between new piece and existing piece
- Captured pieces flip to player's color
- If no valid move, pass
- Game ends when board full or both pass
- Most pieces wins

## Requirements

1. Board representation
2. Valid moves for player
3. Make move (place + flip)
4. Detect game over
5. Score
6. AI player (optional)

## Examples

```python
# Reversi game
game = ReversiGame()
game.make_move(3, 2, Player.BLACK)  # Valid move
game.make_move(4, 2, Player.WHITE)  # Valid move, flips black

game.valid_moves(Player.BLACK)  # => [(2, 2), (5, 3), ...]
game.score()  # => (2, 2)  # black, white
```

## TDD Steps

1. Initial board setup
2. Valid moves from initial position
3. Make move, flip pieces
4. Horizontal capture
5. Vertical capture
6. Diagonal capture
7. Multiple directions at once
8. Pass when no moves
9. Game over detection
10. Scoring