# FizzBuzz Kata

Source: https://github.com/garora/TDD-Katas#the-fizzbuzz-kata

## Problem

Print numbers 1 to 100, but:
- Multiples of 3 → "Fizz"
- Multiples of 5 → "Buzz"
- Multiples of both → "FizzBuzz"

## Requirements

1. `fizzbuzz(n)` returns string for single number
2. `fizzbuzz_range(1, 100)` returns list/prints
3. Extensible: add new rules (e.g., 7 → "Bang")

## Examples

```python
fizzbuzz(1)   # => "1"
fizzbuzz(3)   # => "Fizz"
fizzbuzz(5)   # => "Buzz"
fizzbuzz(15)  # => "FizzBuzz"

fizzbuzz_range(1, 15)
# => ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
```

## TDD Steps

1. 1 → "1"
2. 3 → "Fizz"
3. 5 → "Buzz"
4. 15 → "FizzBuzz"
5. 2 → "2"
6. Range 1-15
7. Custom rules

## Extensions

- Configurable rules (divisor → word)
- FizzBuzzBang (3,5,7)
- FizzBuzzTree (binary tree traversal)
- Parallel FizzBuzz