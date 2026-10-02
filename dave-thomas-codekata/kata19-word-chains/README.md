# Kata19: Word Chains

Source: http://codekata.com/kata/kata19-word-chains/

## Problem

Find the shortest transformation chain between two words, changing one letter at a time, where each intermediate step is a valid word.

## Example

COLD → CORD → CARD → WARD → WARM

## Goals

- Model as graph problem (words = nodes, one-letter-diff = edges)
- Find shortest path (BFS)
- Handle large dictionaries efficiently
- Support variations

## Algorithms

- **BFS** for shortest path (unweighted graph)
- **Bidirectional BFS** for speed
- **A*** with heuristic (letters different)
- Precompute adjacency for repeated queries

## Examples

```python
# Word chain
chain = word_chain("COLD", "WARM", dictionary)
# => ["COLD", "CORD", "CARD", "WARD", "WARM"]

# Bidirectional BFS is faster for long chains
```

## Exercises

1. Basic word ladder (same length words)
2. Allow insert/delete (Levenshtein distance 1)
3. Find all shortest paths
4. Longest possible chain
5. Word ladder puzzle generator
6. Multi-threaded solver
7. Dictionary preprocessing (build graph once)
8. Wildcard patterns (C?LD matches COLD, CORD, etc.)