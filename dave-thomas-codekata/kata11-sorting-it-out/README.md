# Kata11: Sorting It Out

Source: http://codekata.com/kata/kata11-sorting-it-out/

## Problem

Explore different sorting algorithms and their characteristics. Implement multiple sorts and understand when each is appropriate.

## Goals

- Implement 5+ sorting algorithms
- Understand time/space complexity
- Identify stable vs unstable sorts
- Benchmark on different data patterns

## Algorithms to Implement

1. **Bubble Sort** — O(n²), stable, in-place
2. **Insertion Sort** — O(n²), stable, in-place, fast for small/nearly-sorted
3. **Selection Sort** — O(n²), unstable, in-place
4. **Merge Sort** — O(n log n), stable, O(n) space
5. **Quick Sort** — O(n log n) avg, O(n²) worst, unstable, in-place
6. **Heap Sort** — O(n log n), unstable, in-place
7. **Tim Sort** — hybrid (Python/Java standard)
8. **Radix Sort** — O(nk), stable, non-comparison

## Examples

```python
# Sorting algorithms
arr = [64, 34, 25, 12, 22, 11, 90]

bubble_sort(arr.copy())      # => [11, 12, 22, 25, 34, 64, 90]
quick_sort(arr.copy())       # => [11, 12, 22, 25, 34, 64, 90]
merge_sort(arr.copy())       # => [11, 12, 22, 25, 34, 64, 90]
radix_sort([170, 45, 75, 90, 802, 24, 2, 66])  # => [2, 24, 45, 66, 75, 90, 170, 802]
```

## Exercises

1. Implement each with clean, readable code
2. Add instrumentation (comparisons, swaps, recursive calls)
3. Benchmark: random, sorted, reverse, nearly-sorted, many duplicates
4. Visualize sorting process
5. External sort (larger than memory)
6. Parallel merge sort