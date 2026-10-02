# Doublets

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/doublets

## Problem

Find the shortest chain of words connecting two words, where each step changes exactly one letter and forms a valid word. (Also known as "Word Ladders" — Lewis Carroll invented this game.)

## Example

```
HEAD
HEAL
TEAL
TELL
TALL
TAIL
```

## Goals

- Load dictionary
- Build word graph (neighbors differ by 1 letter)
- Find shortest path (BFS)
- Handle different word lengths

## Exercises

1. Basic word ladder (same length)
2. Allow insert/delete (edit distance 1)
3. All shortest paths
4. Longest possible chain in dictionary
5. Bidirectional BFS for speed
6. A* with heuristic
7. Generate puzzles with unique solutions