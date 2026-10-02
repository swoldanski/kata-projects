# Kata18: Transitive Dependencies

Source: http://codekata.com/kata/kata18-transitive-dependencies/

## Problem

Given a dependency graph (package manager, module system, build system), compute transitive closure and detect cycles.

## Goals

- Represent dependency graphs
- Compute transitive dependencies
- Detect circular dependencies
- Topological sort for build order
- Visualize dependency tree

## Algorithms

- **DFS** for cycle detection
- **Kahn's algorithm** for topological sort
- **Tarjan's** for strongly connected components
- **Transitive closure**: Floyd-Warshall, or repeated DFS

## Examples

```python
# Dependency resolution
deps = {
    "app": ["web", "db"],
    "web": ["http", "router"],
    "db": ["pool", "driver"],
    "http": [],
    "router": [],
    "pool": [],
    "driver": [],
}

order = topological_sort(deps)
# => ["http", "router", "web", "pool", "driver", "db", "app"]

cycles = find_cycles(deps)
# => []
```

## Exercises

1. Parse dependency file (package.json, Cargo.toml, go.mod, pom.xml)
2. Build adjacency list
3. Detect cycles, report cycle path
4. Topological sort for install/build order
5. Transitive deps of a given package
6. Reverse dependencies (dependents)
7. Visualize: GraphViz DOT, Mermaid, interactive web
8. Diamond dependency detection
9. Version conflict resolution