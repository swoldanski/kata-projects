# Kata08: Conflicting Objectives

Source: http://codekata.com/kata/kata08-conflicting-objectives/

## Problem

Explore the tradeoffs when you have multiple, conflicting optimization objectives. For example: fast vs. memory-efficient, simple vs. flexible, consistent vs. available (CAP theorem).

## Goals

- Identify conflicting objectives in a real system
- Implement multiple solutions optimizing for different objectives
- Measure and compare the tradeoffs
- Document when each approach is appropriate

## Example Scenarios

1. **Cache eviction**: LRU (recency) vs LFU (frequency) vs ARC (adaptive)
2. **Database indexing**: B-tree (range queries) vs Hash (point lookups) vs LSM (write-heavy)
3. **Serialization**: JSON (readable) vs Protobuf (compact) vs MessagePack (balanced)
4. **Consistency models**: Strong vs Eventual vs Causal

## Examples

```python
# Cache eviction tradeoffs
class Cache:
    def __init__(self, strategy: str):  # "lru", "lfu", "arc"
        self.strategy = strategy
    
    def get(self, key):
        # Implementation varies by strategy
        pass

# LRU: O(1) access, O(1) eviction, recency bias
# LFU: O(1) access, frequency bias, more memory
# ARC: Adaptive, combines LRU+LFU, complex
```

## Exercises

1. Pick a domain (web server, database, compiler, etc.)
2. Identify 2-3 conflicting objectives
3. Implement 2+ approaches optimizing for different objectives
4. Benchmark and visualize tradeoffs
5. Write decision guide: when to use which