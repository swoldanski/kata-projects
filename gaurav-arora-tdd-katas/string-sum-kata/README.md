# String Sum Kata

Source: https://github.com/garora/TDD-Katas#string-sum-kata

## Problem

Create a function that takes a string of numbers separated by commas and returns their sum.

## Requirements

1. Empty string returns 0
2. Single number returns that number
3. Two numbers, comma-separated, returns sum
4. Any amount of numbers
5. Handle newlines as separators too: "1\n2,3" = 6
6. Support custom delimiters: "//;\n1;2" = 3
7. Negative numbers throw exception with all negatives listed
8. Ignore numbers > 1000
9. Delimiters can be any length: "//[***]\n1***2***3" = 6
10. Multiple delimiters: "//[*][%]\n1*2%3" = 6

## Examples

```python
# String sum
string_sum("")           # => 0
string_sum("1")          # => 1
string_sum("1,2")        # => 3
string_sum("1,2,3,4")    # => 10
string_sum("1\n2,3")     # => 6
string_sum("//;\n1;2")   # => 3
```

## TDD Approach

Write tests first, then implement:
1. Empty string
2. Single number
3. Two numbers
4. Multiple numbers
5. Newlines
6. Custom delimiter
7. Negative handling
8. >1000 ignored
9. Multi-char delimiter
10. Multiple delimiters