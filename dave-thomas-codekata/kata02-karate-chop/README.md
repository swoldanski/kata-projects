# Kata02: Karate Chop

Source: http://codekata.com/kata/kata02-karate-chop/

## Problem

A binary chop (sometimes called the more prosaic binary search) finds the position of value in a sorted array of values. It achieves some efficiency by halving the number of items under consideration each time it probes the values: in the first pass it determines whether the required value is in the top or the bottom half of the list of values. In the second pass it considers only this half, again dividing it in to two. It stops when it finds the value it is looking for, or when it runs out of array to search.

**This Kata is straightforward.** Implement a binary search routine in the language and technique of your choice. Tomorrow, implement it again, using a totally different technique. Do the same the next day, until you have **five totally unique implementations** of a binary chop.

For example:
- Traditional iterative approach
- Recursive approach
- Functional style passing array slices around
- Using built-in library functions
- Tail-recursive version

## Goals

This Kata has three separate goals:

1. **Error tracking**: As you're coding each algorithm, keep a note of the kinds of error you encounter. A binary search is a ripe breeding ground for "off by one" and fencepost errors. As you progress through the week, see if the frequency of these errors decreases (that is, do you learn from experience in one technique when it comes to coding with a different technique?).

2. **Technique comparison**: What can you say about the relative merits of the various techniques you've chosen? Which is the most likely to make it in to production code? Which was the most fun to write? Which was the hardest to get working? And for all these questions, ask yourself "why?".

3. **Creativity**: It's fairly hard to come up with five unique approaches to a binary chop. How did you go about coming up with approaches four and five? What techniques did you use to fire those "off the wall" neurons?

## Specification

Write a binary chop method that takes an integer search target and a sorted array of integers. It should return the integer index of the target in the array, or -1 if the target is not in the array.

```
chop(int, array_of_int) -> int
```

## Example

```python
chop(3, [])          # => -1
chop(3, [1])         # => -1
chop(1, [1])         # => 0
chop(1, [1, 3, 5])   # => 0
chop(3, [1, 3, 5])   # => 1
chop(5, [1, 3, 5])   # => 2
chop(0, [1, 3, 5])   # => -1
chop(2, [1, 3, 5])   # => -1
chop(4, [1, 3, 5])   # => -1
chop(6, [1, 3, 5])   # => -1
```