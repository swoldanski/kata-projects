# Kata20: Klondike

Source: http://codekata.com/kata/kata20-klondike/

## Problem

Implement the classic Klondike Solitaire (Windows Solitaire) game logic.

## Goals

- Model game state (tableau, foundation, stock, waste)
- Implement all valid moves
- Detect win/lose conditions
- Support undo/redo
- (Optional) AI solver / hint system

## Rules Summary

- **Tableau**: 7 piles, 1-7 cards, top face up
- **Foundation**: 4 piles (A-K by suit)
- **Stock**: remaining cards, draw 1 or 3
- **Waste**: drawn cards, top playable
- **Moves**: 
  - Tableau → Tableau (descending, alternating color)
  - Tableau → Foundation (ascending, same suit)
  - Waste → Tableau/Foundation
  - Stock → Waste (draw)
  - Foundation → Tableau (rare, usually not allowed)

## Examples

```python
# Klondike game
game = KlondikeGame()
game.deal_new()

# Move: tableau pile 1 -> foundation
game.move(TableauPile(1), Foundation(Suit.HEARTS))

# Auto-complete obvious moves
game.auto_complete()
```

## Exercises

1. Data structures for game state
2. Move validation
3. Move execution with undo
4. Auto-complete (move to foundation when obvious)
5. Win detection
6. Deal new game (shuffle, deal)
7. Statistics tracking
8. Hint system (suggest move)
9. Text-based or GUI interface
10. Solver: can this game be won?