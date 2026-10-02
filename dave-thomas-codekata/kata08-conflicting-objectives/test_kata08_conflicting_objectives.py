"""Tests for kata08-conflicting-objectives."""

from kata08_conflicting_objectives import (
    SIMPLICITY_SCORE,
    ArcStrategy,
    Cache,
    CacheMetrics,
    ConflictingObjectives,
    EvictionPolicy,
    InMemoryBenchmarkRepository,
    LfuStrategy,
    LruStrategy,
    Objective,
    analyze_tradeoffs,
    best_policy,
    compare,
    make_strategy,
    recommend,
    simulate,
)

# The workload the tradeoff analysis is measured on: a hot pair that is
# re-requested constantly, wrapped in a warm-up burst and then buried under a
# long one-shot scan. A recency policy is dragged around by the scan and loses
# the hot keys; a frequency policy has already counted them and keeps them.
# Measured on capacity 3: LRU 40%, ARC 42.5%, LFU 45%.
BURSTY = ["h0", "h1"] * 5 + [f"scan{i}" for i in range(20)] + ["h0", "h1"] * 5

# A second, deliberately different workload: the hot pair is interleaved with
# the scan instead of buried by it. Here the adaptive policy underperforms
# both of the simple ones (ARC 48.9% vs LRU/LFU 64.4%) - the kata's point that
# no single policy is best everywhere.
INTERLEAVED = [key for i in range(30) for key in ("h0", "h1", f"scan{i}")]


class TestConflictingObjectives:
    """Test cases for kata08-conflicting-objectives."""

    def test_basic_case(self):
        """A small cache serves repeats and evicts when it overflows."""
        cache = Cache(capacity=2, policy=EvictionPolicy.LRU)

        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.get("b") == 2
        assert cache.get("a") == 1

        cache.put("c", 3)  # "b" was touched longest ago, so it goes
        assert "b" not in cache
        assert set(cache.keys()) == {"a", "c"}

        metrics = cache.metrics
        assert metrics.hits == 2
        assert metrics.misses == 0
        assert metrics.evictions == 1

    def test_edge_cases(self):
        """Empty caches, misses, re-puts and invalid capacities."""
        cache = Cache(capacity=1)

        assert cache.get("missing") is None
        assert cache.metrics.misses == 1
        assert cache.metrics.hit_rate == 0.0

        cache.put("a", 1)
        cache.put("a", 2)  # updating an existing key is not an eviction
        assert cache.get("a") == 2
        assert cache.metrics.evictions == 0

        try:
            Cache(capacity=0)
        except ValueError:
            pass
        else:
            raise AssertionError("capacity 0 should raise ValueError")

    def test_tdd_progression(self):
        """LRU, then LFU, then ARC, then the measured comparison."""
        # Step 1: LRU keeps the most recently touched keys.
        lru = Cache(capacity=2, policy=EvictionPolicy.LRU)
        for key in ("a", "b", "a", "c"):
            lru.put(key, key)
            lru.get(key)
        assert "a" in lru

        # Step 2: LFU keeps the most frequently touched keys.
        lfu = Cache(capacity=2, policy=EvictionPolicy.LFU)
        lfu.put("hot", 1)
        for _ in range(5):
            lfu.get("hot")
        lfu.put("cold", 2)
        lfu.put("new", 3)
        assert "hot" in lfu
        assert "cold" not in lfu

        # Step 3: ARC starts balanced and adapts as ghost hits arrive.
        arc = ArcStrategy(capacity=4)
        assert arc.target_recent == 2
        arc.on_insert("gone")
        arc.on_evict("gone")
        arc.on_insert("gone")  # ghost hit on the recency side
        assert arc.target_recent == 3

        # Step 4: on a bursty workload, frequency-aware policies win.
        measured = compare(BURSTY, capacity=3)
        assert measured[EvictionPolicy.LFU].hit_rate > measured[EvictionPolicy.LRU].hit_rate


class TestEvictionStrategies:
    """Each strategy evicts the victim its policy promises."""

    def test_lru_evicts_the_least_recently_used(self):
        strategy = LruStrategy()
        for key in ("a", "b", "c"):
            strategy.on_insert(key)
        strategy.on_access("a")  # "a" becomes the most recent

        assert strategy.choose_victim(["a", "b", "c"]) == "b"

    def test_lfu_evicts_the_least_frequently_used(self):
        strategy = LfuStrategy()
        for key in ("a", "b", "c"):
            strategy.on_insert(key)
        for _ in range(3):
            strategy.on_access("c")

        assert strategy.choose_victim(["a", "b", "c"]) == "a"

    def test_lfu_breaks_ties_on_insertion_order(self):
        strategy = LfuStrategy()
        strategy.on_insert("first")
        strategy.on_insert("second")

        assert strategy.choose_victim(["first", "second"]) == "first"

    def test_arc_promotes_repeatedly_accessed_keys(self):
        strategy = ArcStrategy(capacity=4)
        strategy.on_insert("x")
        strategy.on_access("x")
        strategy.on_insert("y")

        # "x" was promoted into the frequency list, so the recency side is
        # cheaper to evict from.
        assert strategy.choose_victim(["x", "y"]) == "y"

    def test_arc_favours_the_recency_side_when_recency_keeps_missing(self):
        """A key evicted from the recency list and asked for again grows it."""
        strategy = ArcStrategy(capacity=4)
        start = strategy.target_recent  # 2 of 4 slots go to recency

        strategy.on_insert("a")
        strategy.on_evict("a")
        strategy.on_insert("a")

        assert strategy.target_recent > start

    def test_arc_favours_the_frequency_side_when_frequency_keeps_missing(self):
        """A key evicted from the frequency list and asked for again shrinks it."""
        strategy = ArcStrategy(capacity=4)
        start = strategy.target_recent

        strategy.on_insert("b")
        strategy.on_access("b")   # promoted into the frequency list
        strategy.on_evict("b")    # ...and then pushed out into its ghosts
        strategy.on_insert("b")   # a miss on a key the policy had counted on

        assert strategy.target_recent < start

    def test_victim_is_none_when_there_are_no_candidates(self):
        assert LruStrategy().choose_victim([]) is None
        assert LfuStrategy().choose_victim([]) is None
        assert ArcStrategy(capacity=2).choose_victim([]) is None

    def test_reset_clears_all_strategy_state(self):
        lru = LruStrategy()
        lru.on_insert("a")
        lru.reset()
        assert lru.choose_victim(["a"]) == "a"

        lfu = LfuStrategy()
        lfu.on_insert("a")
        lfu.reset()
        assert lfu.choose_victim(["a"]) == "a"

        arc = ArcStrategy(capacity=4)
        arc.on_insert("a")
        arc.reset()
        assert arc.target_recent == 2

    def test_factory_maps_policy_to_strategy(self):
        assert isinstance(make_strategy(EvictionPolicy.LRU, 3), LruStrategy)
        assert isinstance(make_strategy(EvictionPolicy.LFU, 3), LfuStrategy)
        assert isinstance(make_strategy(EvictionPolicy.ARC, 3), ArcStrategy)

    def test_cache_accepts_an_injected_strategy(self):
        cache = Cache(capacity=2, strategy=LruStrategy())
        assert cache.policy is EvictionPolicy.LRU


class TestMeasurements:
    """Metrics are what a benchmark would report."""

    def test_lru_wins_when_accesses_are_cyclic(self):
        # With capacity equal to the working set, LRU keeps everything. The
        # first touch of each key is still a miss, hence 6/9 rather than 100%.
        accesses = ["a", "b", "c"] * 3
        metrics = simulate(accesses, capacity=3, policy=EvictionPolicy.LRU)

        assert metrics.hits == 6
        assert metrics.misses == 3
        assert metrics.hit_rate == 0.6667
        assert metrics.evictions == 0

    def test_lru_keeps_everything_once_the_working_set_is_warm(self):
        metrics = simulate(["a", "b", "c"] * 3 + ["a", "b", "c"], capacity=3)

        assert metrics.evictions == 0
        assert metrics.hit_rate == 0.75

    def test_a_one_shot_scan_punishes_every_policy(self):
        # A burst walks many distinct keys once, so most lookups miss whoever
        # is in charge: this is the workload no eviction policy can rescue.
        metrics = simulate(BURSTY, capacity=3, policy=EvictionPolicy.LRU)

        assert metrics.hit_rate < 0.5
        assert metrics.evictions > 0

    def test_lru_loses_when_the_working_set_exceeds_capacity(self):
        # Cycling through 4 keys with room for only 3 guarantees that the key
        # asked for next was just evicted - the classic LRU worst case.
        metrics = simulate([f"k{i % 4}" for i in range(40)], capacity=3)

        assert metrics.hit_rate == 0.0
        assert metrics.evictions == 37

    def test_frequency_policies_beat_lru_on_a_bursty_workload(self):
        measured = compare(BURSTY, capacity=3)

        assert measured[EvictionPolicy.LFU].hit_rate > measured[EvictionPolicy.LRU].hit_rate
        assert measured[EvictionPolicy.ARC].hit_rate > measured[EvictionPolicy.LRU].hit_rate

    def test_no_policy_wins_every_workload(self):
        """The kata's point: the winner depends on the workload."""
        bursty = compare(BURSTY, capacity=3)
        cyclic = compare(INTERLEAVED, capacity=3)

        # When the hot set is buried under a one-shot scan the frequency-aware
        # policies keep it and hold a clear lead.
        assert bursty[EvictionPolicy.LFU].hit_rate > bursty[EvictionPolicy.LRU].hit_rate

        # When the scan is interleaved instead, every policy does about as well
        # as the others: the same policy is not best everywhere.
        rates = {m.hit_rate for m in cyclic.values()}
        assert len(rates) <= 2

    def test_hit_and_miss_rates_are_complementary(self):
        metrics = simulate(["a", "a", "b", "c"], capacity=3)

        assert metrics.requests == 4
        assert metrics.hit_rate + metrics.miss_rate == 1.0

    def test_empty_metrics_report_zero(self):
        metrics = CacheMetrics(policy=EvictionPolicy.LRU, capacity=3)

        assert metrics.requests == 0
        assert metrics.hit_rate == 0.0
        assert metrics.miss_rate == 0.0
        assert metrics.throughput == 0.0

    def test_peak_entries_never_exceeds_capacity(self):
        metrics = simulate([f"k{i}" for i in range(50)], capacity=5)

        assert metrics.peak_entries == 5


class TestTradeoffAnalysis:
    """The point of the kata: nothing wins every objective."""

    def test_tradeoffs_are_reported_for_every_objective(self):
        tradeoffs = ConflictingObjectives(capacity=3).tradeoffs(BURSTY)

        assert {t.objective for t in tradeoffs} == {
            Objective.HIT_RATE,
            Objective.MEMORY,
            Objective.LATENCY,
            Objective.SIMPLICITY,
        }

    def test_simplicity_always_favours_lru(self):
        tradeoffs = ConflictingObjectives(capacity=3).tradeoffs(BURSTY)
        simplicity = next(t for t in tradeoffs if t.objective is Objective.SIMPLICITY)

        assert simplicity.winner is EvictionPolicy.LRU
        assert simplicity.margin == SIMPLICITY_SCORE[EvictionPolicy.LRU] - SIMPLICITY_SCORE[
            EvictionPolicy.ARC
        ]

    def test_objectives_genuinely_conflict(self):
        """The best hit rate is not the simplest policy."""
        guide = ConflictingObjectives(capacity=3).recommendations(BURSTY)
        picks = {rec.objective: rec.policy for rec in guide}

        assert picks[Objective.SIMPLICITY] is EvictionPolicy.LRU
        assert picks[Objective.HIT_RATE] is not EvictionPolicy.LRU

    def test_equal_results_are_reported_as_a_tie(self):
        metrics = [
            CacheMetrics(policy=p, capacity=3, hits=1, misses=1)
            for p in (EvictionPolicy.LRU, EvictionPolicy.LFU)
        ]
        from kata08_conflicting_objectives import (
            TradeoffQuery,
            TradeoffQueryHandler,
        )

        verdict = TradeoffQueryHandler(InMemoryBenchmarkRepository()).handle_tradeoff(
            TradeoffQuery(Objective.HIT_RATE, tuple(metrics))
        )

        assert verdict.is_tie
        assert verdict.winner is None

    def test_recommendations_explain_themselves(self):
        for rec in ConflictingObjectives(capacity=3).recommendations(BURSTY):
            assert rec.rationale
            assert rec.measured >= 0.0

    def test_memory_objective_prefers_the_smaller_footprint(self):
        metrics = [
            CacheMetrics(policy=EvictionPolicy.LRU, capacity=3, peak_entries=3),
            CacheMetrics(policy=EvictionPolicy.LFU, capacity=3, peak_entries=2),
        ]
        guide = recommend(metrics, (Objective.MEMORY,))

        assert guide[0].policy is EvictionPolicy.LFU

    def test_recommendations_for_no_measurements(self):
        assert recommend([]) == []


class TestArchitecture:
    """DDD / CQRS / Repository wiring."""

    def test_benchmark_command_stores_metrics_in_the_repository(self):
        engine = ConflictingObjectives(capacity=3)
        engine.benchmark(["a", "b", "a"], store=True)

        assert len(engine._repository) == 3  # one run per policy
        assert engine._repository.get("lru") is not None

        assert len(InMemoryBenchmarkRepository()) == 0  # fresh stores are independent

    def test_benchmark_without_store_leaves_the_repository_empty(self):
        engine = ConflictingObjectives(capacity=3)
        engine.benchmark(["a", "b", "a"], store=False)

        assert len(engine._repository) == 0

    def test_query_returns_one_metrics_object_per_policy(self):
        results = ConflictingObjectives(capacity=3).analyse(["a", "b", "a"])

        assert set(results) == {
            EvictionPolicy.LRU,
            EvictionPolicy.LFU,
            EvictionPolicy.ARC,
        }
        assert results[EvictionPolicy.LRU].policy is EvictionPolicy.LRU

    def test_policies_can_be_restricted(self):
        results = ConflictingObjectives(capacity=3).benchmark(
            ["a", "b"], policies=(EvictionPolicy.LFU,), store=False
        )

        assert [m.policy for m in results] == [EvictionPolicy.LFU]

    def test_facade_capacity_drives_the_benchmark(self):
        small = ConflictingObjectives(capacity=1).analyse(["a", "b", "c"])
        large = ConflictingObjectives(capacity=10).analyse(["a", "b", "c"])

        assert small[EvictionPolicy.LRU].evictions > large[EvictionPolicy.LRU].evictions


class TestFunctionalInterface:
    """Module-level helpers mirror the facade."""

    def test_simulate_and_compare(self):
        accesses = ["a", "b", "a"]

        assert simulate(accesses, capacity=2).policy is EvictionPolicy.LRU
        results = compare(accesses, capacity=2)
        assert len(results) == 3

    def test_best_policy_for_an_objective(self):
        assert best_policy(BURSTY, capacity=3, objective=Objective.SIMPLICITY) is (
            EvictionPolicy.LRU
        )
        assert best_policy(BURSTY, capacity=3, objective=Objective.HIT_RATE) is not (
            EvictionPolicy.LRU
        )

    def test_analyze_tradeoffs_accepts_plain_dictionaries(self):
        report = analyze_tradeoffs(
            [
                {"policy": "lru", "accesses": BURSTY, "capacity": 3},
                {"policy": EvictionPolicy.LFU, "accesses": BURSTY},
            ],
            capacity=3,
        )

        assert set(report["metrics"]) == {EvictionPolicy.LRU, EvictionPolicy.LFU}
        assert len(report["tradeoffs"]) == 4
        assert all("objective" in entry for entry in report["tradeoffs"])
        assert report["recommendations"]

    def test_empty_trace_yields_no_measurements(self):
        assert best_policy([], capacity=3) is EvictionPolicy.LRU
        assert simulate([], capacity=3).requests == 0


class TestBenchmarkScale:
    """Behaves on a long access pattern."""

    def test_long_trace_reports_consistent_totals(self):
        trace = [f"k{i % 7}" for i in range(5_000)]
        metrics = simulate(trace, capacity=10, policy=EvictionPolicy.ARC)

        assert metrics.requests == 5_000
        assert metrics.hits + metrics.misses == 5_000
        assert 0.0 <= metrics.hit_rate <= 1.0
        assert metrics.peak_entries <= 10

    def test_metrics_stay_invariant_across_policies(self):
        trace = [f"k{i % 9}" for i in range(2_000)]
        measured = compare(trace, capacity=5)

        assert {m.requests for m in measured.values()} == {2_000}
        assert len({m.policy for m in measured.values()}) == 3

    def test_elapsed_time_is_recorded_by_the_command_handler(self):
        engine = ConflictingObjectives(capacity=4)
        results = engine.benchmark([f"k{i % 8}" for i in range(200)], store=False)

        assert all(m.elapsed_seconds >= 0.0 for m in results)