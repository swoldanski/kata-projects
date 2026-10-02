"""Tests for kata06-anagrams."""

from kata06_anagrams import (
    AnagramGroup,
    AnagramService,
    AnagramStats,
    Anagrams,
    InMemoryAnagramRepository,
    SignatureStrategy,
    Word,
    count_anagram_groups,
    find_anagram_sets,
    group_anagrams,
    largest_anagram_group,
    timed_group,
)


class TestAnagrams:
    """Test cases for kata06-anagrams."""

    def test_basic_case(self):
        """Group the README example."""
        words = ["listen", "silent", "enlist", "hello", "world", "dlrow"]

        groups = group_anagrams(words)
        normalized = sorted(tuple(sorted(g)) for g in groups)

        assert normalized == [
            ("dlrow", "world"),
            ("enlist", "listen", "silent"),
            ("hello",),
        ]

    def test_edge_cases(self):
        """Empty input, duplicates, single words and non-words."""
        assert group_anagrams([]) == []

        # A duplicate word is an anagram of itself and stays in the group.
        groups = group_anagrams(["cat", "cat"])
        assert [sorted(g) for g in groups] == [["cat", "cat"]]

        # Whitespace is stripped, and words under min_length are dropped.
        service = AnagramService(min_length=3)
        groups = service.group_as_lists([" ab ", "ba", "abc", "cba"])
        assert [sorted(g) for g in groups] == [["abc", "cba"]]

    def test_tdd_progression(self):
        """Grow from one group, to several, to filtering and statistics."""
        # Step 1: a single pair.
        assert largest_anagram_group(["cat", "act", "dog"]) == ["cat", "act"]

        # Step 2: several groups.
        assert count_anagram_groups(["cat", "act", "dog", "god", "zebra"]) == 2

        # Step 3: only real anagram sets (size >= 2) are reported.
        assert find_anagram_sets(["cat", "act", "dog"]) == [["cat", "act"]]

        # Step 4: statistics summarise the dictionary.
        stats = AnagramService().stats(["cat", "act", "dog", "god", "zebra"])
        assert stats.total_words == 5
        assert stats.total_groups == 3
        assert stats.anagram_groups == 2
        assert stats.largest_group_size == 2


class TestSignatureStrategies:
    """All signature strategies must group identically."""

    def test_strategies_agree(self):
        words = ["listen", "silent", "enlist", "cat", "act", "zebra", "hello"]
        expected = sorted(
            tuple(sorted(g))
            for g in AnagramService(SignatureStrategy.SORTED).group_as_lists(words)
        )

        for strategy in SignatureStrategy:
            service = AnagramService(strategy)
            assert sorted(
                tuple(sorted(g)) for g in service.group_as_lists(words)
            ) == expected

    def test_word_signature_is_order_independent(self):
        assert Word("listen").signature() == Word("silent").signature()
        assert Word("Listen").signature() == "eilnst"

    def test_word_rejects_empty(self):
        try:
            Word("")
        except ValueError as exc:
            assert "empty" in str(exc)
        else:
            raise AssertionError("Word('') should raise ValueError")

    def test_strategy_used_by_service(self):
        service = AnagramService(SignatureStrategy.PRIME)
        assert service.strategy is SignatureStrategy.PRIME


class TestAnagramGroup:
    """AnagramGroup behaves like the aggregate it models."""

    def test_group_reports_membership_and_size(self):
        group = AnagramGroup(signature="act", words=("cat", "act", "tac"))

        assert len(group) == 3
        assert group.size == 3
        assert group.word_length == 3
        assert group.is_anagram_set() is True
        assert group.contains("CAT") is True
        assert group.contains("dog") is False
        assert list(group) == ["cat", "act", "tac"]

    def test_singleton_is_not_an_anagram_set(self):
        group = AnagramGroup(signature="dog", words=("dog",))
        assert group.is_anagram_set() is False


class TestArchitecture:
    """DDD / CQRS / Repository wiring."""

    def test_command_stores_groups_in_repository(self):
        engine = Anagrams()
        words = ["cat", "act", "dog"]

        engine.group(words, store=True)

        repository = InMemoryAnagramRepository()
        assert len(repository) == 0  # a fresh repository is independent

        engine2 = Anagrams()
        engine2.group(words, store=True)
        assert engine2.find_anagrams("cat") == ["act"]

    def test_query_finds_anagrams_of_stored_word(self):
        engine = Anagrams()
        engine.group(["listen", "silent", "enlist", "zebra"], store=True)

        assert sorted(engine.find_anagrams("listen")) == ["enlist", "silent"]
        assert engine.find_anagrams("zebra") == []
        assert engine.find_anagrams("unknown") == []

    def test_find_anagrams_without_stored_data(self):
        engine = Anagrams()
        assert engine.find_anagrams("cat") == []

    def test_stats_and_largest_via_facade(self):
        engine = Anagrams()
        words = ["cat", "act", "tac", "dog", "god", "zebra"]

        largest = engine.largest_group(words)
        assert largest is not None
        assert sorted(largest.words) == ["act", "cat", "tac"]

        assert engine.word_with_most_anagrams(words) == ("cat", 3)
        assert engine.stats(words).anagram_groups == 2

    def test_service_is_shared_by_handlers(self):
        """A service built with a minimum length drives the facade."""
        engine = Anagrams(min_length=4)
        assert engine.group_anagrams(["cat", "act", "tale", "late"]) == [
            ["tale", "late"]
        ]


class TestFunctionalInterface:
    """Module-level helpers mirror the facade."""

    def test_functional_helpers(self):
        words = ["listen", "silent", "dog", "god", "zebra"]

        assert count_anagram_groups(words) == 2
        assert sorted(tuple(sorted(g)) for g in find_anagram_sets(words)) == [
            ("dog", "god"),
            ("listen", "silent"),
        ]
        assert sorted(largest_anagram_group(words)) == ["listen", "silent"]

    def test_timed_group_returns_groups_and_duration(self):
        groups, elapsed = timed_group(["cat", "act", "dog"])

        assert len(groups) == 2
        assert elapsed >= 0.0

    def test_largest_group_is_empty_without_anagrams(self):
        assert largest_anagram_group(["cat", "dog"]) == []
        assert count_anagram_groups(["cat", "dog"]) == 0


class TestDictionaryScale:
    """Behaves on a large, repetitive dictionary."""

    def test_groups_large_word_list(self):
        # Every index owns a unique multiset of three letters, so each
        # spelling is an anagram of only its twin.
        letters = "abcdefghijklmnopqrstuvwxyz"
        multisets = [
            a + b + c
            for a in letters for b in letters for c in letters
            if a < b < c
        ][:2000]
        words = [f"zz{ms}" for ms in multisets] + [f"zz{ms[::-1]}" for ms in multisets]

        groups = AnagramService().group(words)
        stats = AnagramService().stats(words)

        assert stats.total_words == 4000
        assert stats.anagram_groups == 2000
        assert stats.largest_group_size == 2
        assert len(groups) == 2000
        assert all(g.is_anagram_set() for g in groups)

    def test_groups_repeated_letters(self):
        # Letters repeated across words still group correctly.
        groups = AnagramService().group_as_lists(["abba", "baba", "baab", "abab"])
        assert [sorted(g) for g in groups] == [["abab", "abba", "baab", "baba"]]

    def test_stats_ratio_for_empty_input(self):
        stats = AnagramService().stats([])
        assert stats == AnagramStats(
            total_words=0, total_groups=0, anagram_groups=0,
            largest_group_size=0, total_signatures_processed=0,
        )
        assert stats.grouped_word_ratio == 0.0