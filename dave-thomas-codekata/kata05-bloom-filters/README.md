# Kata05: Bloom Filters

Source: http://codekata.com/kata/kata05-bloom-filters/

## Problem

A Bloom filter is a space-efficient probabilistic data structure used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not — in other words, a query returns either "possibly in set" or "definitely not in set".

## Goals

- Implement a Bloom filter from scratch
- Understand the tradeoffs between:
  - Size of the bit array
  - Number of hash functions
  - False positive rate
- Experiment with different hash functions
- Test with various data sets (dictionary words, URLs, etc.)

## Key Concepts

- **Bit array**: Fixed-size array of bits, initially all 0
- **Hash functions**: k independent hash functions that map elements to array positions
- **Insert**: Set bits at all k positions to 1
- **Query**: Check if all k positions are 1 (possibly in set) or any is 0 (definitely not in set)

## False Positive Probability

For a Bloom filter with:
- m = bits in array
- n = elements inserted
- k = hash functions

Optimal k = (m/n) * ln(2)
False positive rate ≈ (1 - e^(-kn/m))^k

## Examples

```python
# Bloom Filter usage
bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
bf.add("hello")
bf.add("world")
"hello" in bf  # True (maybe)
"goodbye" in bf  # False (definitely not)
```

## Exercises

1. Basic implementation with fixed parameters
2. Parameterized version (choose m, n, k)
3. Test false positive rate empirically
4. Compare with other probabilistic structures (Cuckoo filters, etc.)
5. Use case: spell checker, URL deduplication, cache filtering