# Kata13: Counting Code Lines

Source: http://codekata.com/kata/kata13-counting-code-lines/

## Problem

Write a tool that counts lines of code in a project, distinguishing between:
- Code lines
- Comment lines
- Blank lines
- (Optionally) docstrings, string literals

## Goals

- Handle multiple languages
- Accurate counting (not fooled by comments in strings)
- Configurable rules per language
- Fast on large codebases

## Examples

```python
# Line counting
counts = count_lines("my_project/")
# => {"code": 1523, "comments": 342, "blank": 187, "total": 2052}

# Per-language
counts = count_lines("my_project/", languages=["python", "javascript"])
```

## Exercises

1. Basic line counter (code/comment/blank)
2. Language detection by extension
3. Handle language-specific comment syntax:
   - `//` and `/* */` (C, Java, JS, Go, Rust)
   - `#` (Python, Ruby, Shell)
   - `--` (SQL, Lua, Haskell)
   - `;` (Lisp, Assembly)
   - `<!-- -->` (HTML, XML)
4. Exclude string literals from comment counting
5. Count logical lines vs physical lines
6. Directory traversal with .gitignore support
7. Output formats: text, JSON, CSV, HTML
8. Compare with tools: cloc, tokei, scc