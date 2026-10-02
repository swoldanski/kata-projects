# Kata14: Tom Swift Under the Milkwood

Source: http://codekata.com/kata/kata14-tom-swift-under-the-milkwood/

## Problem

Generate "Tom Swifties" — puns where an adverb describes how something is said, relating to the quote:

> "I love hot dogs," Tom said frankly.

## Goals

- Build a generator for wordplay/puns
- Explore linguistic patterns
- Have fun with language

## Structure

A Tom Swifty has:
- A quote
- A speaker (traditionally "Tom")
- An adverb that puns on the quote content

## Examples

- "I dropped the toothpaste," Tom said **crestfallen**.
- "I forgot the bread," Tom said **loafingly**.
- "This vacuum is loud," Tom said **suctionally**.

## Examples

```python
# Tom Swifty generator
tom_swifty = TomSwifty()
tom_swifty.add_pair("I dropped the toothpaste", "crestfallen")
tom_swifty.add_pair("I forgot the bread", "loafingly")

print(tom_swifty.generate("I lost my flashlight"))
# => "I lost my flashlight," Tom said darkly.
```

## Exercises

1. Curate a list of (quote, adverb) pairs
2. Template-based generation
3. NLP approach: find adverbs related to quote keywords
4. Interactive: user provides quote, system suggests adverbs
5. Score/rate generated puns
6. Extend to other pun formats