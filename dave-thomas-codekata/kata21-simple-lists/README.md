# Kata21: Simple Lists

Source: http://codekata.com/kata/kata21-simple-lists/

## Problem

Implement a linked list data structure from scratch, with all standard operations.

## Goals

- Understand pointer/reference manipulation
- Implement core operations efficiently
- Compare with array-based lists
- Explore variations (doubly-linked, circular, skip list)

## Operations

- **Insert**: at head, tail, position, after node
- **Delete**: by value, by position, head, tail
- **Search**: find, find by index
- **Traverse**: forward, backward (doubly)
- **Utility**: length, reverse, clear, clone
- **Advanced**: sort, merge, dedupe, split

## Variations

1. **Singly linked** — next pointer only
2. **Doubly linked** — prev + next
3. **Circular** — tail.next = head
4. **Skip list** — probabilistic balanced structure
5. **Persistent** — immutable, structural sharing

## Examples

```python
# Linked list
ll = LinkedList()
ll.append(1).append(2).append(3)
ll.prepend(0)
# => 0 -> 1 -> 2 -> 3

ll.reverse()
# => 3 -> 2 -> 1 -> 0

# Cycle detection
ll.append(ll.head)  # Create cycle
ll.has_cycle()  # => True (Floyd's algorithm)
```

## Exercises

1. Singly linked list with all basic ops
2. Doubly linked list
3. Circular buffer using linked list
4. Implement iterator protocol
5. Merge two sorted lists
6. Detect cycle (Floyd's algorithm)
7. Reverse in-place (iterative and recursive)
8. Benchmark vs array list
9. Skip list implementation