#!/usr/bin/env python3
"""Generate Python starter templates for all katas."""

from pathlib import Path

KATA_ROOT = Path(__file__).parent

# Template for kata implementation
KATA_TEMPLATE = '''"""{{kata_name}} - {{description}}

{{source}}
"""

from typing import List, Optional


# TODO: Implement the kata here
# Follow DDD, CQRS, Repository patterns with in-memory state
# No database, no ORM, no external persistence


def {{main_function}}({{params}}) -> {{return_type}}:
    """{{function_docstring}}"""
    raise NotImplementedError("Implement {{kata_name}}")
'''

# Template for kata tests
TEST_TEMPLATE = '''"""Tests for {{kata_name}}."""

import pytest
from {{module_name}} import {{main_function}}


class Test{{class_name}}:
    """Test cases for {{kata_name}}."""

    def test_basic_case(self):
        """Test basic functionality."""
        # TODO: Add test cases based on kata examples
        raise NotImplementedError("Add test cases")

    def test_edge_cases(self):
        """Test edge cases."""
        raise NotImplementedError("Add edge case tests")
'''

# Dave Thomas katas are named kataNN-...; to_class_name() strips that prefix.
DAVE_THOMAS_KATA_IDS = {f"kata{n:02d}" for n in range(1, 22)}

# Kata specifications: (directory_name, description, main_function, params,
# return_type, function_docstring, class_name)
KATAS = [
    # Dave Thomas CodeKata
    ("dave-thomas-codekata/kata01-supermarket-pricing", "Supermarket Pricing - Design kata (no code)", "design_pricing_model", "", "dict", "Return a design document for pricing models", "SupermarketPricing"),  # noqa: E501
    ("dave-thomas-codekata/kata02-karate-chop", "Karate Chop - Binary search with 5 implementations", "chop", "target: int, arr: List[int]", "int", "Return index of target in sorted array, or -1", "KarateChop"),  # noqa: E501
    ("dave-thomas-codekata/kata03-how-big-how-fast", "How Big? How Fast? - Estimation exercises", "estimate_bits", "n: int", "int", "Estimate bits needed for unsigned representation of n", "HowBigHowFast"),  # noqa: E501
    ("dave-thomas-codekata/kata04-data-munging", "Data Munging - Weather and soccer data parsing", "find_min_spread_day", "weather_data: str", "int", "Return day with smallest temperature spread", "DataMunging"),  # noqa: E501
    ("dave-thomas-codekata/kata05-bloom-filters", "Bloom Filters - Probabilistic data structure", "BloomFilter", "", "None", "Bloom filter implementation", "BloomFilters"),  # noqa: E501
    ("dave-thomas-codekata/kata06-anagrams", "Anagrams - Group words by anagram", "group_anagrams", "words: List[str]", "List[List[str]]", "Group words into anagram sets", "Anagrams"),  # noqa: E501
    ("dave-thomas-codekata/kata07-howd-i-do", "How'd I Do? - Quiz scoring system", "score_quiz", "answers: List[str], key: List[str]", "int", "Calculate quiz score", "HowdIDo"),  # noqa: E501
    ("dave-thomas-codekata/kata08-conflicting-objectives", "Conflicting Objectives - Tradeoff analysis", "analyze_tradeoffs", "options: List[dict]", "dict", "Analyze conflicting objectives", "ConflictingObjectives"),  # noqa: E501
    ("dave-thomas-codekata/kata09-back-to-the-checkout", "Back to the Checkout - Supermarket checkout", "Checkout", "", "None", "Checkout system with pricing rules", "BackToCheckout"),  # noqa: E501
    ("dave-thomas-codekata/kata10-hashes-vs-classes", "Hashes vs Classes - Data vs behavior", "Order", "", "None", "Order as class vs hash comparison", "HashesVsClasses"),  # noqa: E501
    ("dave-thomas-codekata/kata11-sorting-it-out", "Sorting It Out - Multiple sorting algorithms", "sort", "arr: List[int], algorithm: str", "List[int]", "Sort using specified algorithm", "SortingItOut"),  # noqa: E501
    ("dave-thomas-codekata/kata12-best-sellers", "Best Sellers - Top-K streaming", "TopK", "", "None", "Maintain top K items from stream", "BestSellers"),  # noqa: E501
    ("dave-thomas-codekata/kata13-counting-code-lines", "Counting Code Lines - LOC counter", "count_lines", "path: str", "dict", "Count code/comment/blank lines", "CountingCodeLines"),  # noqa: E501
    ("dave-thomas-codekata/kata14-tom-swift-under-the-milkwood", "Tom Swifties - Pun generator", "generate_tom_swifty", "quote: str", "str", "Generate Tom Swifty pun", "TomSwifties"),  # noqa: E501
    ("dave-thomas-codekata/kata15-a-diversion", "A Diversion - Open-ended kata", "diversion", "", "None", "Open-ended diversion", "ADiversion"),  # noqa: E501
    ("dave-thomas-codekata/kata16-business-rules", "Business Rules - Rules engine", "RulesEngine", "", "None", "Business rules engine", "BusinessRules"),  # noqa: E501
    ("dave-thomas-codekata/kata17-more-business-rules", "More Business Rules - Advanced rules", "AdvancedRulesEngine", "", "None", "Advanced business rules", "MoreBusinessRules"),  # noqa: E501
    ("dave-thomas-codekata/kata18-transitive-dependencies", "Transitive Dependencies - Dependency graph", "resolve_dependencies", "deps: dict", "List[str]", "Resolve transitive dependencies", "TransitiveDependencies"),  # noqa: E501
    ("dave-thomas-codekata/kata19-word-chains", "Word Chains - Word ladder", "word_chain", "start: str, end: str, dictionary: List[str]", "List[str]", "Find shortest word chain", "WordChains"),  # noqa: E501
    ("dave-thomas-codekata/kata20-klondike", "Klondike - Solitaire game", "KlondikeGame", "", "None", "Klondike solitaire implementation", "Klondike"),  # noqa: E501
    ("dave-thomas-codekata/kata21-simple-lists", "Simple Lists - Linked list implementation", "LinkedList", "", "None", "Linked list data structure", "SimpleLists"),  # noqa: E501

    # Gaurav Arora TDD Katas
    ("gaurav-arora-tdd-katas/string-sum-kata", "String Sum - Sum numbers in string", "string_sum", "s: str", "int", "Sum comma-separated numbers", "StringSum"),  # noqa: E501
    ("gaurav-arora-tdd-katas/string-calculator-kata", "String Calculator - TDD classic", "add", "numbers: str", "int", "Add numbers from string with delimiters", "StringCalculator"),  # noqa: E501
    ("gaurav-arora-tdd-katas/bowling-game-kata", "Bowling Game - Ten-pin scoring", "BowlingGame", "", "None", "Score a bowling game", "BowlingGame"),  # noqa: E501
    ("gaurav-arora-tdd-katas/fizzbuzz-kata", "FizzBuzz - Classic kata", "fizzbuzz", "n: int", "str", "Return FizzBuzz for n", "FizzBuzz"),  # noqa: E501
    ("gaurav-arora-tdd-katas/oddeven-kata", "OddEven - Partition numbers", "partition_oddeven", "numbers: List[int]", "tuple", "Return (odds, evens)", "OddEven"),  # noqa: E501
    ("gaurav-arora-tdd-katas/prime-factor-kata", "Prime Factors - Prime factorization", "prime_factors", "n: int", "List[int]", "Return prime factors of n", "PrimeFactor"),  # noqa: E501
    ("gaurav-arora-tdd-katas/game-of-life", "Game of Life - Cellular automaton", "GameOfLife", "", "None", "Conway's Game of Life", "GameOfLife"),  # noqa: E501
    ("gaurav-arora-tdd-katas/harry-potter", "Harry Potter - Book discount pricing", "calculate_price", "books: List[int]", "float", "Calculate price with discounts", "HarryPotter"),  # noqa: E501
    ("gaurav-arora-tdd-katas/lcd-digits", "LCD Digits - 7-segment display", "lcd_display", "number: str, size: int", "str", "Render number as LCD", "LCDDigits"),  # noqa: E501
    ("gaurav-arora-tdd-katas/leap-year", "Leap Year - Gregorian calendar", "is_leap_year", "year: int", "bool", "Check if leap year", "LeapYear"),  # noqa: E501
    ("gaurav-arora-tdd-katas/mine-fields", "Mine Fields - Minesweeper generator", "generate_field", "width: int, height: int, mines: int", "List[str]", "Generate minesweeper field", "MineFields"),  # noqa: E501
    ("gaurav-arora-tdd-katas/poker-hands", "Poker Hands - Hand ranking", "compare_hands", "hand1: str, hand2: str", "str", "Compare two poker hands", "PokerHands"),  # noqa: E501
    ("gaurav-arora-tdd-katas/recently-used-list", "Recently Used List - LRU cache", "RecentlyUsedList", "capacity: int", "None", "LRU-style recently used list", "RecentlyUsedList"),  # noqa: E501
    ("gaurav-arora-tdd-katas/reversi", "Reversi - Othello game logic", "ReversiGame", "", "None", "Reversi/Othello implementation", "Reversi"),  # noqa: E501
    ("gaurav-arora-tdd-katas/yahtzee", "Yahtzee - Dice game scoring", "score_category", "category: str, dice: List[int]", "int", "Score Yahtzee category", "Yahtzee"),  # noqa: E501
    ("gaurav-arora-tdd-katas/word-wrap-kata", "Word Wrap - Text wrapping", "wrap", "text: str, width: int", "str", "Wrap text to width", "WordWrap"),  # noqa: E501

    # Wonderland Clojure Katas
    ("wonderland-clojure-katas/alphabet-cipher", "Alphabet Cipher - Substitution cipher", "AlphabetCipher", "keyword: str", "None", "Substitution cipher with keyword", "AlphabetCipher"),  # noqa: E501
    ("wonderland-clojure-katas/card-game-war", "Card Game War - War simulation", "play_war", "", "dict", "Simulate War card game", "CardGameWar"),  # noqa: E501
    ("wonderland-clojure-katas/doublets", "Doublets - Word ladders", "find_doublet_chain", "start: str, end: str, dictionary: List[str]", "List[str]", "Find word ladder", "Doublets"),  # noqa: E501
    ("wonderland-clojure-katas/fox-goose-bag-of-corn", "Fox Goose Bag of Corn - River crossing", "solve_river_crossing", "", "List[str]", "Solve river crossing puzzle", "FoxGooseBagOfCorn"),  # noqa: E501
    ("wonderland-clojure-katas/magic-square", "Magic Square - Generate magic squares", "generate_magic_square", "n: int", "List[List[int]]", "Generate NxN magic square", "MagicSquare"),  # noqa: E501
    ("wonderland-clojure-katas/tiny-maze", "Tiny Maze - Maze generation/solving", "Maze", "width: int, height: int", "None", "Maze generation and solving", "TinyMaze"),  # noqa: E501
    ("wonderland-clojure-katas/wonderland-number", "Wonderland Number - Number sequences", "generate_sequence", "name: str, n: int", "List[int]", "Generate number sequence", "WonderlandNumber"),  # noqa: E501

    # SensioLabs PoleDev Katas
    ("sensiolabs-poledev-katas/kata-data-transformer", "Data Transformer - Format conversion", "DataTransformer", "", "None", "Transform data between formats", "DataTransformer"),  # noqa: E501
    ("sensiolabs-poledev-katas/kata-event-listener", "Event Listener - Event dispatcher", "EventDispatcher", "", "None", "Event dispatcher/observer pattern", "EventListener"),  # noqa: E501
    ("sensiolabs-poledev-katas/kata-inherit-data", "Inherit Data - Form inheritance", "Form", "", "None", "Form inheritance with virtual fields", "InheritData"),  # noqa: E501
    ("sensiolabs-poledev-katas/kata-upload-file", "File Upload - Upload handler", "FileUploadHandler", "", "None", "Secure file upload handling", "FileUpload"),  # noqa: E501
    ("sensiolabs-poledev-katas/kata-translation", "Translation - i18n management", "TranslationManager", "", "None", "Translation management system", "Translation"),  # noqa: E501
]


def to_module_name(kata_path: str) -> str:
    """Convert kata path to module name."""
    return kata_path.split("/")[-1].replace("-", "_")


def to_class_name(kata_path: str) -> str:
    """Convert kata path to class name."""
    name = kata_path.split("/")[-1]
    parts = name.split("-")
    if parts[0] in DAVE_THOMAS_KATA_IDS:
        # Dave Thomas katas - use the descriptive part
        desc = "-".join(parts[1:])
        return "".join(p.capitalize() for p in desc.split("-"))
    return "".join(p.capitalize() for p in name.split("-"))


def generate_kata_files(
    kata_path: str,
    description: str,
    main_function: str,
    params: str,
    return_type: str,
    function_docstring: str,
    class_name: str,
) -> None:
    """Generate kata implementation and test files."""
    full_path = KATA_ROOT / kata_path
    module_name = to_module_name(kata_path)

    # Implementation file
    impl_file = full_path / f"{module_name}.py"
    impl_content = f'''"""{{kata_name}} - {{description}}

Source: {{source}}
"""

from __future__ import annotations

from typing import Any


# TODO: Implement the kata here
# Follow DDD, CQRS, Repository patterns with in-memory state
# No database, no ORM, no external persistence
# Use domain entities, value objects, aggregates, domain services
# Separate commands (writes) from queries (reads)
# Abstract data access behind repository interfaces
# Use in-memory collections (lists, dicts, sets) for state


def {main_function}({params}) -> {return_type}:
    """{{function_docstring}}"""
    raise NotImplementedError("Implement {main_function}")


class {class_name}:
    """{{function_docstring}}"""

    def __init__(self) -> None:
        raise NotImplementedError("Implement {{class_name}}")
'''.format(
        kata_name=kata_path.split("/")[-1],
        description=description,
        source="See README.md",
        class_name=class_name,
        main_function=main_function,
        params=params,
        return_type=return_type,
        function_docstring=function_docstring,
    )

    impl_file.write_text(impl_content)

    # Test file
    test_file = full_path / f"test_{module_name}.py"
    test_content = f'''"""Tests for {kata_path.split("/")[-1]}."""

from {module_name} import {class_name}, {main_function}


class Test{class_name}:
    """Test cases for {kata_path.split("/")[-1]}."""

    def test_basic_case(self):
        """Test basic functionality."""
        # TODO: Add test cases based on kata examples in README.md
        raise NotImplementedError("Add test cases from README examples")

    def test_edge_cases(self):
        """Test edge cases."""
        raise NotImplementedError("Add edge case tests")

    def test_tdd_progression(self):
        """Test following TDD progression from README."""
        raise NotImplementedError("Follow TDD steps from README")
'''
    test_file.write_text(test_content)

    print(f"Generated: {impl_file.relative_to(KATA_ROOT)}")  # noqa: T201
    print(f"Generated: {test_file.relative_to(KATA_ROOT)}")  # noqa: T201


def main():
    """Generate all kata templates."""
    for kata_spec in KATAS:
        generate_kata_files(*kata_spec)
    print(f"\nGenerated templates for {len(KATAS)} katas")  # noqa: T201


if __name__ == "__main__":
    main()