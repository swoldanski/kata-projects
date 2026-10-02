# Kata07: How'd I Do?

Source: http://codekata.com/kata/kata07-howd-i-do/

## Problem

Implement a simple scoring system for a quiz or test. Given a set of questions with answers and a student's responses, calculate their score.

## Goals

- Model questions, answers, and scoring rules
- Support different question types (multiple choice, true/false, short answer)
- Handle partial credit
- Generate feedback/report

## Examples

```python
# Quiz scoring
quiz = Quiz()
quiz.add_question("What is 2+2?", "4", type="short")
quiz.add_question("Capital of France?", "Paris", type="short", case_insensitive=True)

score = quiz.score({"What is 2+2?": "4", "Capital of France?": "paris"})
# => 2/2 correct
```

## Exercises

1. Basic scoring: exact match for multiple choice
2. Case-insensitive string matching for short answers
3. Partial credit for "close" answers
4. Weighted questions
5. Bonus questions
6. Generate detailed report (which questions wrong, why)
7. Support different grading scales (percentage, letter grade, GPA)