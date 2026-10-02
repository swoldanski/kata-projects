# Tiny Maze

Source: https://github.com/gigasquid/wonderland-clojure-katas/tree/master/tiny-maze

## Problem

Generate and solve small mazes. Practice graph algorithms and grid-based pathfinding.

## Goals

- Maze generation algorithms
- Pathfinding (BFS, DFS, A*, Dijkstra)
- Visualization

## Generation Algorithms

1. **Recursive Backtracker** (DFS) — perfect mazes
2. **Prim's Algorithm** — minimum spanning tree
3. **Kruskal's Algorithm** — randomized MST
4. **Aldous-Broder** — uniform spanning tree
5. **Wilson's Algorithm** — loop-erased random walk
6. **Eller's Algorithm** — row-by-row, memory efficient

## Solving Algorithms

1. **Wall Follower** (left/right hand rule)
2. **BFS** — shortest path (unweighted)
3. **DFS** — finds a path, not necessarily shortest
4. **A*** — with Manhattan/Euclidean heuristic
5. **Dijkstra** — weighted grids

## Examples

```python
# Maze generation and solving
maze = Maze(10, 10)
maze.generate()  # DFS backtracker

solution = maze.solve()  # BFS shortest path
# => [(0, 0), (1, 0), (1, 1), ..., (9, 9)]
```

## Exercises

1. Generate perfect maze (DFS)
2. Solve with BFS
3. Visualize generation step-by-step
4. Multiple start/end points
5. Maze with loops (braid mazes)
6. 3D maze
7. Maze editor