"""kata06-anagrams - Anagrams

Group words into anagram sets (words sharing the same letter multiset).

Source: http://codekata.com/kata/kata06-anagrams/

Architecture: DDD + CQRS + Repository, in-memory state only.
"""

from __future__ import annotations

import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

# =============================================================================
# Value Objects
# =============================================================================

class SignatureStrategy(Enum):
    """Ways to derive an order-independent signature for a word."""
    SORTED = "sorted"           # sort the letters
    PRIME = "prime"             # product of per-letter primes
    COUNT = "count"             # 26-element letter counts
    FROZEN_COUNTER = "frozen"   # frozen Counter of letters


_PRIME_BY_LETTER: dict[str, int] = {}
_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
]
for _i, _ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
    _PRIME_BY_LETTER[_ch] = _PRIMES[_i]


@dataclass(frozen=True)
class Word:
    """A word, normalized for anagram comparison."""
    text: str

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("Word cannot be empty")

    @property
    def normalized(self) -> str:
        """Lower-cased form used for signature generation."""
        return self.text.lower()

    @property
    def length(self) -> int:
        return len(self.text)

    def signature(self, strategy: SignatureStrategy = SignatureStrategy.SORTED) -> str:
        """Order-independent signature for grouping anagrams."""
        w = self.normalized
        if strategy is SignatureStrategy.SORTED:
            return "".join(sorted(w))
        if strategy is SignatureStrategy.PRIME:
            product = 1
            for ch in w:
                prime = _PRIME_BY_LETTER.get(ch)
                if prime is None:
                    # non a-z characters cannot be prime-encoded; fall back
                    return "".join(sorted(w))
                product *= prime
            return str(product)
        if strategy is SignatureStrategy.COUNT:
            counts = [0] * 26
            for ch in w:
                idx = ord(ch) - ord("a")
                if 0 <= idx < 26:
                    counts[idx] += 1
            return ",".join(str(c) for c in counts)
        if strategy is SignatureStrategy.FROZEN_COUNTER:
            return repr(sorted(Counter(w).items()))
        raise ValueError(f"Unknown strategy: {strategy}")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.text


@dataclass(frozen=True)
class AnagramGroup:
    """An aggregate of words that are anagrams of one another."""
    signature: str
    words: tuple[str, ...]

    @property
    def size(self) -> int:
        return len(self.words)

    @property
    def word_length(self) -> int:
        return len(self.words[0]) if self.words else 0

    def is_anagram_set(self) -> bool:
        """A real anagram set has at least two members."""
        return self.size >= 2

    def contains(self, word: str) -> bool:
        return word.lower() in {w.lower() for w in self.words}

    def __iter__(self):
        return iter(self.words)

    def __len__(self) -> int:
        return self.size


@dataclass(frozen=True)
class AnagramStats:
    """Statistics computed over a collection of anagram groups."""
    total_words: int
    total_groups: int
    anagram_groups: int
    largest_group_size: int
    total_signatures_processed: int

    @property
    def grouped_word_ratio(self) -> float:
        if self.total_words == 0:
            return 0.0
        return self.anagram_groups / self.total_words


# =============================================================================
# Domain Service
# =============================================================================

class AnagramService:
    """Domain service: groups words into anagram sets."""

    def __init__(self, strategy: SignatureStrategy = SignatureStrategy.SORTED,
                 min_length: int = 1, case_sensitive: bool = False):
        self._strategy = strategy
        self._min_length = min_length
        self._case_sensitive = case_sensitive

    @property
    def strategy(self) -> SignatureStrategy:
        return self._strategy

    def _key(self, raw: str) -> str:
        word = raw if self._case_sensitive else raw.lower()
        if self._strategy is SignatureStrategy.SORTED:
            return "".join(sorted(word))
        return Word(word).signature(self._strategy)

    def group(self, words: list[str]) -> list[AnagramGroup]:
        """Group words into AnagramGroup aggregates.

        Words shorter than ``min_length`` are ignored. Duplicates are kept
        (they are themselves anagrams of each other).
        """
        buckets: dict[str, list[str]] = {}
        for raw in words:
            raw = raw.strip()
            if len(raw) < self._min_length:
                continue
            buckets.setdefault(self._key(raw), []).append(raw)
        return [
            AnagramGroup(signature=sig, words=tuple(members))
            for sig, members in buckets.items()
        ]

    def group_as_lists(self, words: list[str]) -> list[list[str]]:
        """Group words, returning plain nested lists."""
        groups = self.group(words)
        return [list(g.words) for g in groups]

    def anagram_sets(self, words: list[str]) -> list[AnagramGroup]:
        """Only groups that actually contain anagrams (size >= 2)."""
        return [g for g in self.group(words) if g.is_anagram_set()]

    def largest_group(self, words: list[str]) -> AnagramGroup | None:
        """The anagram group with the most words (ties broken by first seen)."""
        groups = self.group(words)
        if not groups:
            return None
        return max(groups, key=lambda g: g.size)

    def longest_anagram_group(self, words: list[str]) -> AnagramGroup | None:
        """Anagram group with the longest words, then the largest."""
        groups = [g for g in self.group(words) if g.is_anagram_set()]
        if not groups:
            return None
        return max(groups, key=lambda g: (g.word_length, g.size))

    def word_with_most_anagrams(self, words: list[str]) -> tuple[str, int] | None:
        """Return (word, count) for the word in the biggest anagram set."""
        largest = self.largest_group(words)
        if largest is None or not largest.is_anagram_set():
            return None
        return (largest.words[0], largest.size)

    def stats(self, words: list[str]) -> AnagramStats:
        """Compute summary statistics for a word list."""
        groups = self.group(words)
        anagram_groups = [g for g in groups if g.is_anagram_set()]
        return AnagramStats(
            total_words=sum(g.size for g in groups),
            total_groups=len(groups),
            anagram_groups=len(anagram_groups),
            largest_group_size=max((g.size for g in groups), default=0),
            total_signatures_processed=len(groups),
        )


# =============================================================================
# Repository
# =============================================================================

class AnagramRepository(Protocol):
    """Repository interface for anagram groups."""

    def save(self, group: AnagramGroup) -> None: ...
    def load(self, signature: str) -> AnagramGroup | None: ...
    def all(self) -> list[AnagramGroup]: ...
    def clear(self) -> None: ...


class InMemoryAnagramRepository:
    """In-memory repository keyed by signature."""

    def __init__(self):
        self._groups: dict[str, AnagramGroup] = {}

    def save(self, group: AnagramGroup) -> None:
        self._groups[group.signature] = group

    def load(self, signature: str) -> AnagramGroup | None:
        return self._groups.get(signature)

    def all(self) -> list[AnagramGroup]:
        return list(self._groups.values())

    def clear(self) -> None:
        self._groups.clear()

    def __len__(self) -> int:
        return len(self._groups)


# =============================================================================
# Commands & Queries (CQRS)
# =============================================================================

@dataclass
class GroupAnagramsCommand:
    words: list[str]
    store: bool = False


@dataclass
class FindAnagramsQuery:
    word: str


@dataclass
class LargestGroupQuery:
    words: list[str]


@dataclass
class StatsQuery:
    words: list[str]


class AnagramCommandHandler:
    """Handles write-side operations."""

    def __init__(self, service: AnagramService, repository: AnagramRepository):
        self._service = service
        self._repository = repository

    def handle_group(self, cmd: GroupAnagramsCommand) -> list[AnagramGroup]:
        groups = self._service.group(cmd.words)
        if cmd.store:
            for g in groups:
                self._repository.save(g)
        return groups


class AnagramQueryHandler:
    """Handles read-side operations."""

    def __init__(self, service: AnagramService, repository: AnagramRepository):
        self._service = service
        self._repository = repository

    def handle_find(self, query: FindAnagramsQuery) -> list[str]:
        for group in self._repository.all():
            if group.contains(query.word):
                return [w for w in group.words if w.lower() != query.word.lower()]
        return []

    def handle_largest(self, query: LargestGroupQuery) -> AnagramGroup | None:
        return self._service.largest_group(query.words)

    def handle_stats(self, query: StatsQuery) -> AnagramStats:
        return self._service.stats(query.words)


# =============================================================================
# Facade
# =============================================================================

class Anagrams:
    """Main facade for anagram grouping."""

    def __init__(self, strategy: SignatureStrategy = SignatureStrategy.SORTED,
                 min_length: int = 1, case_sensitive: bool = False):
        self._service = AnagramService(strategy, min_length, case_sensitive)
        self._repository = InMemoryAnagramRepository()
        self._command_handler = AnagramCommandHandler(self._service, self._repository)
        self._query_handler = AnagramQueryHandler(self._service, self._repository)

    # Commands
    def group(self, words: list[str], store: bool = False) -> list[AnagramGroup]:
        return self._command_handler.handle_group(
            GroupAnagramsCommand(words=words, store=store)
        )

    def group_anagrams(self, words: list[str]) -> list[list[str]]:
        """Group words into plain nested lists (kata's primary API)."""
        return self._service.group_as_lists(words)

    # Queries
    def find_anagrams(self, word: str) -> list[str]:
        if not self._repository.all():
            return []
        return self._query_handler.handle_find(FindAnagramsQuery(word=word))

    def largest_group(self, words: list[str]) -> AnagramGroup | None:
        return self._query_handler.handle_largest(LargestGroupQuery(words=words))

    def longest_anagram_group(self, words: list[str]) -> AnagramGroup | None:
        return self._service.longest_anagram_group(words)

    def word_with_most_anagrams(self, words: list[str]) -> tuple[str, int] | None:
        return self._service.word_with_most_anagrams(words)

    def stats(self, words: list[str]) -> AnagramStats:
        return self._query_handler.handle_stats(StatsQuery(words=words))


# =============================================================================
# Functional interface
# =============================================================================

def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words into anagram sets, returning plain nested lists."""
    return AnagramService().group_as_lists(words)


def find_anagram_sets(words: list[str]) -> list[list[str]]:
    """Only the groups that contain real anagrams (size >= 2)."""
    return [list(g.words) for g in AnagramService().anagram_sets(words)]


def largest_anagram_group(words: list[str]) -> list[str]:
    """The largest anagram set (empty list if none has anagrams)."""
    group = AnagramService().largest_group(words)
    if group is None or not group.is_anagram_set():
        return []
    return list(group.words)


def count_anagram_groups(words: list[str]) -> int:
    """Number of groups that contain real anagrams."""
    return len(AnagramService().anagram_sets(words))


def timed_group(words: list[str],
                strategy: SignatureStrategy = SignatureStrategy.SORTED
                ) -> tuple[list[AnagramGroup], float]:
    """Group words and return (groups, elapsed_seconds)."""
    start = time.perf_counter()
    groups = AnagramService(strategy).group(words)
    return groups, time.perf_counter() - start


# =============================================================================
# Example Usage & Demo
# =============================================================================

if __name__ == "__main__":
    print("=== Kata06: Anagrams - Demo ===\n")

    sample = [
        "listen", "silent", "enlist", "hello", "world", "dlrow",
        "cat", "act", "tac", "dog", "god", "odg", "zebra",
    ]

    engine = Anagrams()
    print("Groups:")
    for group in engine.group(sample):
        marker = "*" if group.is_anagram_set() else " "
        print(f"  {marker} {list(group.words)}")

    print(f"\nGroups with real anagrams: {count_anagram_groups(sample)}")
    largest = engine.largest_group(sample)
    print(f"Largest group: {list(largest.words) if largest else []}")
    print(f"Longest anagram group: {engine.longest_anagram_group(sample)}")
    print(f"Stats: {engine.stats(sample)}")

    print("\nStrategy comparison (should group identically):")
    for strategy in SignatureStrategy:
        groups = AnagramService(strategy).group_as_lists(sample)
        print(f"  {strategy.value:8} -> {sorted(map(sorted, groups))}")