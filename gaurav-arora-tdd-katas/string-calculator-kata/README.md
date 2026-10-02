# String Calculator Kata (via Roy Osherove)

Source: https://github.com/garora/TDD-Katas#string-calculator-kata-via-roy-osherove

## Problem

Same as String Sum Kata — this is the classic Roy Osherove String Calculator kata.

## Requirements

1. **Empty string** → 0
2. **Single number** → that number
3. **Two numbers, comma delimited** → sum
4. **Multiple numbers** → sum
5. **Newlines as separators** → "1\n2,3" = 6
6. **Custom delimiter** → "//;\n1;2" = 3
7. **Negative numbers** → throw exception "negatives not allowed: -1,-3"
8. **Numbers > 1000 ignored** → 2 + 1001 = 2
9. **Multi-char delimiters** → "//[***]\n1***2***3" = 6
10. **Multiple delimiters** → "//[*][%]\n1*2%3" = 6

## Examples

```python
add("")              # => 0
add("1")             # => 1
add("1,2")           # => 3
add("1,2,3")         # => 6
add("1\n2,3")        # => 6
add("//;\n1;2")      # => 3
add("2,1001")        # => 2 (ignores >1000)
add("//[***]\n1***2") # => 3
add("//[*][%]\n1*2%3") # => 6
```

## TDD Steps

Follow the exact order above. Each step adds one test, then implementation.

## Refactoring Points

- Extract delimiter parsing
- Separate validation from calculation
- Consider strategy pattern for delimiters