# Word Wrap Kata

Source: http://codingdojo.org/cgi-bin/wiki.pl?KataWordWrap

## Problem

Wrap text to a given column width, breaking at word boundaries.

## Requirements

1. `wrap(text, width)` → wrapped text
2. Break at spaces (not mid-word)
3. Long words: break at width (or keep whole word)
4. Preserve paragraphs (blank lines)
5. Handle tabs, multiple spaces

## Examples

```
wrap("The quick brown fox", 10)
→ "The quick\nbrown fox"

wrap("Hello world", 5)
→ "Hello\nworld"
```

## TDD Steps

1. Empty string → ""
2. Short text (fits) → unchanged
3. Exact width → unchanged
4. One break needed
5. Multiple breaks
6. Word longer than width
7. Paragraphs
8. Tabs/spaces