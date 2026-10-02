# Kata06: Anagrams

Source: http://codekata.com/kata/kata06-anagrams/

## Problem

Given a dictionary of words, find all sets of anagrams (words that use the same letters in a different order).

## Goals

- Efficiently group words by their "signature" (sorted letters)
- Handle large dictionaries (100k+ words)
- Consider memory vs. speed tradeoffs
- Output: groups of anagrams, largest group, words with most anagrams

## Approaches

1. **Sort-and-group**: Sort letters of each word, use as dictionary key
2. **Prime factorization**: Map each letter to a prime, multiply for signature
3. **Character count**: Use 26-element count array as key

## Examples

```python
# Anagram grouping
words = ["listen", "silent", "enlist", "hello", "world", "dlrow"]
groups = group_anagrams(words)
# => [["listen", "silent", "enlist"], ["hello"], ["world", "dlrow"]]
```

## Exercises

1. Basic implementation reading from word list
2. Find longest anagram group
3. Find word with most anagrams
4. Handle case insensitivity
5. Filter by word length
6. Performance: time and memory for /usr/share/dict/words
7. Extensions: multi-word anagrams, crossword helpers