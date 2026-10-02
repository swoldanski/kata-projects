"""kata08-conflicting-objectives - Conflicting Objectives - Tradeoff analysis

A cache whose eviction policy is an interchangeable strategy. LRU favours
recent keys, LFU favours frequent keys, ARC adapts between the two. The kata's
point is that no single policy wins everywhere, so the module also ships a
benchmark that measures the tradeoffs on the same access pattern.

Source: http://codekata.com/kata/kata08-conflicting-objectives/

Architecture: DDD + CQRS + Repository, in-memory state only.
"""

from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

# =============================================================================
# Value Objects
# =============================================================================

class EvictionPolicy(Enum):
    """Interchangeable cache eviction strategies."""

    LRU = "lru"   # evict the least recently used key
    LFU = "lfu"   # evict the least frequently used key
    ARC = "arc"   # adapt between recency and frequency


class Objective(Enum):
    """The things a cache designer can optimise, at each other's expense."""

    HIT_RATE = "hit_rate"       # serve as many lookups as possible
    MEMORY = "memory"           # keep the footprint small
    LATENCY = "latency"         # keep lookups cheap and predictable
    SIMPLICITY = "simplicity"   # keep the implementation easy to reason about


@dataclass(frozen=True)
class CacheMetrics:
    """Measured outcome of a cache run."""

    policy: EvictionPolicy
    capacity: int
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    peak_entries: int = 0
    elapsed_seconds: float = 0.0

    @property
    def requests(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        if self.requests == 0:
            return 0.0
        return round(self.hits / self.requests, 4)

    @property
    def miss_rate(self) -> float:
        return round(1.0 - self.hit_rate, 4) if self.requests else 0.0

    @property
    def throughput(self) -> float:
        """Lookups served per second (0.0 when unmeasured)."""
        if self.elapsed_seconds <= 0:
            return 0.0
        return round(self.requests / self.elapsed_seconds, 2)


@dataclass(frozen=True)
class Tradeoff:
    """An objective comparison between two policies."""

    objective: Objective
    winner: EvictionPolicy | None
    margin: float

    @property
    def is_tie(self) -> bool:
        return self.winner is None


@dataclass(frozen=True)
class Recommendation:
    """Decision-guide entry: which policy to pick, and why."""

    objective: Objective
    policy: EvictionPolicy
    rationale: str
    measured: float


# =============================================================================
# Eviction Strategy (domain service contract + implementations)
# =============================================================================

class EvictionStrategy(Protocol):
    """Decides which key leaves the cache when it is full."""

    @property
    def policy(self) -> EvictionPolicy: ...

    def on_insert(self, key: str) -> None: ...

    def on_access(self, key: str) -> None: ...

    def on_evict(self, key: str) -> None: ...

    def choose_victim(self, keys: list[str]) -> str | None: ...

    def reset(self) -> None: ...


class LruStrategy:
    """Least recently used: a recency-ordered access log."""

    _order: OrderedDict[str, None]

    def __init__(self) -> None:
        self._order = OrderedDict()

    @property
    def policy(self) -> EvictionPolicy:
        return EvictionPolicy.LRU

    def on_insert(self, key: str) -> None:
        self._order[key] = None

    def on_access(self, key: str) -> None:
        self._order.pop(key, None)
        self._order[key] = None

    def on_evict(self, key: str) -> None:
        self._order.pop(key, None)

    def choose_victim(self, keys: list[str]) -> str | None:
        if not keys:
            return None
        # The first entry in the access log is the least recently used key.
        for candidate in self._order:
            if candidate in keys:
                return candidate
        return keys[0]

    def reset(self) -> None:
        self._order.clear()


class LfuStrategy:
    """Least frequently used: keeps a counter per key."""

    _counts: dict[str, int]
    _insertion_order: list[str]

    def __init__(self) -> None:
        self._counts = {}
        self._insertion_order = []

    @property
    def policy(self) -> EvictionPolicy:
        return EvictionPolicy.LFU

    def on_insert(self, key: str) -> None:
        self._counts[key] = 0
        self._insertion_order.append(key)

    def on_access(self, key: str) -> None:
        self._counts[key] = self._counts.get(key, 0) + 1

    def on_evict(self, key: str) -> None:
        self._counts.pop(key, None)
        if key in self._insertion_order:
            self._insertion_order.remove(key)

    def choose_victim(self, keys: list[str]) -> str | None:
        if not keys:
            return None
        live = [k for k in self._insertion_order if k in keys]
        if not live:
            live = list(keys)
        # Lowest count wins; ties break on the earliest insertion.
        return min(live, key=lambda k: (self._counts.get(k, 0), live.index(k)))

    def reset(self) -> None:
        self._counts.clear()
        self._insertion_order.clear()


class ArcStrategy:
    """Adaptive Replacement Cache.

    Keeps a recency list (T1) and a frequency list (T2). A hit in T2 promotes
    the key, and repeated misses on recently evicted keys grow the frequency
    side, so the policy drifts toward whichever behaviour the workload rewards.
    """

    _recent: OrderedDict[str, None]
    _frequent: OrderedDict[str, None]
    _ghost_recent: list[str]
    _ghost_frequent: list[str]
    _target_recent: int

    def __init__(self, capacity: int = 1) -> None:
        self._capacity = max(1, capacity)
        self._target_recent = max(1, self._capacity // 2)
        self._min_target_recent = 0
        self._recent = OrderedDict()
        self._frequent = OrderedDict()
        self._ghost_recent = []
        self._ghost_frequent = []

    @property
    def policy(self) -> EvictionPolicy:
        return EvictionPolicy.ARC

    @property
    def target_recent(self) -> int:
        """How many slots the adaptive policy currently gives to recency."""
        return self._target_recent

    def on_insert(self, key: str) -> None:
        if key in self._ghost_recent:
            # A miss on a recently evicted key: favour recency.
            self._ghost_recent.remove(key)
            self._target_recent = min(self._capacity, self._target_recent + 1)
        elif key in self._ghost_frequent:
            # A miss on a frequently used key: favour frequency.
            self._ghost_frequent.remove(key)
            self._target_recent = max(self._min_target_recent, self._target_recent - 1)
        self._recent[key] = None

    def on_access(self, key: str) -> None:
        if key in self._recent:
            # Promoted on second access: recency -> frequency.
            self._recent.pop(key)
            self._frequent[key] = None
        elif key in self._frequent:
            self._frequent.pop(key)
            self._frequent[key] = None

    def on_evict(self, key: str) -> None:
        if key in self._recent:
            self._recent.pop(key)
            self._ghost_recent.append(key)
            del self._ghost_recent[: -self._capacity]
        elif key in self._frequent:
            self._frequent.pop(key)
            self._ghost_frequent.append(key)
            del self._ghost_frequent[: -self._capacity]

    def choose_victim(self, keys: list[str]) -> str | None:
        if not keys:
            return None
        # Evict from the side the policy currently favours, i.e. the side it
        # has decided deserves *fewer* slots. Evicting from the frequency side
        # is only right once the recency list has outgrown its target.
        recent = [k for k in self._recent if k in keys]
        frequent = [k for k in self._frequent if k in keys]
        # T1 (recency) is the probationary list: keys there have been asked for
        # only once and are the cheapest to lose. Once T1 has grown past its
        # target the policy must protect T2 instead, so it evicts from there.
        if recent and (not frequent or len(recent) <= self._target_recent):
            return recent[0]
        if frequent:
            return frequent[0]
        return recent[0] if recent else keys[0]

    def reset(self) -> None:
        self._recent.clear()
        self._frequent.clear()
        self._ghost_recent.clear()
        self._ghost_frequent.clear()
        self._target_recent = max(1, self._capacity // 2)


def make_strategy(policy: EvictionPolicy, capacity: int) -> EvictionStrategy:
    """Factory: the policy enum picks the strategy implementation."""
    if policy is EvictionPolicy.LRU:
        return LruStrategy()
    if policy is EvictionPolicy.LFU:
        return LfuStrategy()
    if policy is EvictionPolicy.ARC:
        return ArcStrategy(capacity)
    raise ValueError(f"Unknown policy: {policy}")


# =============================================================================
# Aggregate
# =============================================================================

class Cache:
    """A capacity-bounded cache that delegates eviction to a strategy."""

    _strategy: EvictionStrategy

    def __init__(
        self,
        capacity: int = 3,
        policy: EvictionPolicy = EvictionPolicy.LRU,
        strategy: EvictionStrategy | None = None,
    ) -> None:
        if capacity <= 0:
            raise ValueError("Cache capacity must be positive")
        self.capacity = capacity
        self._entries: dict[str, Any] = {}
        self._strategy = strategy if strategy is not None else make_strategy(policy, capacity)
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._peak_entries = 0

    @property
    def policy(self) -> EvictionPolicy:
        return self._strategy.policy

    @property
    def metrics(self) -> CacheMetrics:
        return CacheMetrics(
            policy=self.policy,
            capacity=self.capacity,
            hits=self._hits,
            misses=self._misses,
            evictions=self._evictions,
            peak_entries=self._peak_entries,
        )

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, key: str) -> bool:
        return key in self._entries

    def keys(self) -> list[str]:
        return list(self._entries)

    def get(self, key: str) -> Any | None:
        """Look up a key, recording a hit or miss."""
        if key in self._entries:
            self._hits += 1
            self._strategy.on_access(key)
            return self._entries[key]
        self._misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """Store a key, evicting a victim first if the cache is full."""
        if key in self._entries:
            self._entries[key] = value
            self._strategy.on_access(key)
            return

        if len(self._entries) >= self.capacity:
            self._evict()
        self._entries[key] = value
        self._strategy.on_insert(key)
        self._peak_entries = max(self._peak_entries, len(self._entries))

    def _evict(self) -> None:
        victim = self._strategy.choose_victim(self.keys())
        if victim is None:
            return
        del self._entries[victim]
        self._strategy.on_evict(victim)
        self._evictions += 1


# =============================================================================
# Repository
# =============================================================================

class BenchmarkRepository(Protocol):
    """Storage abstraction for benchmark runs (in-memory only)."""

    def save(self, name: str, metrics: CacheMetrics) -> None: ...

    def get(self, name: str) -> CacheMetrics | None: ...

    def all(self) -> list[CacheMetrics]: ...

    def __len__(self) -> int: ...


class InMemoryBenchmarkRepository:
    """In-memory store of the metrics produced by benchmark runs."""

    def __init__(self) -> None:
        self._runs: dict[str, CacheMetrics] = {}

    def save(self, name: str, metrics: CacheMetrics) -> None:
        self._runs[name] = metrics

    def get(self, name: str) -> CacheMetrics | None:
        return self._runs.get(name)

    def all(self) -> list[CacheMetrics]:
        return list(self._runs.values())

    def __len__(self) -> int:
        return len(self._runs)


# =============================================================================
# CQRS
# =============================================================================

@dataclass
class BenchmarkCommand:
    accesses: list[str]
    capacity: int = 3
    policies: tuple[EvictionPolicy, ...] = (
        EvictionPolicy.LRU,
        EvictionPolicy.LFU,
        EvictionPolicy.ARC,
    )
    store: bool = False


@dataclass
class TradeoffQuery:
    objective: Objective
    metrics: tuple[CacheMetrics, ...]
    higher_is_better: bool = True


@dataclass
class RecommendationQuery:
    metrics: tuple[CacheMetrics, ...]
    objectives: tuple[Objective, ...] = (
        Objective.HIT_RATE,
        Objective.MEMORY,
        Objective.SIMPLICITY,
    )


class BenchmarkCommandHandler:
    """Write side: run caches over an access pattern."""

    def __init__(self, repository: BenchmarkRepository):
        self._repository = repository

    def handle_benchmark(self, cmd: BenchmarkCommand) -> list[CacheMetrics]:
        results: list[CacheMetrics] = []
        for policy in cmd.policies:
            cache = Cache(capacity=cmd.capacity, policy=policy)
            started = time.perf_counter()
            _replay(cache, cmd.accesses)
            elapsed = time.perf_counter() - started

            raw = cache.metrics
            measured = CacheMetrics(
                policy=raw.policy,
                capacity=raw.capacity,
                hits=raw.hits,
                misses=raw.misses,
                evictions=raw.evictions,
                peak_entries=raw.peak_entries,
                elapsed_seconds=elapsed,
            )
            if cmd.store:
                self._repository.save(policy.value, measured)
            results.append(measured)
        return results


class TradeoffQueryHandler:
    """Read side: compare measured results."""

    def __init__(self, repository: BenchmarkRepository):
        self._repository = repository

    def handle_tradeoff(self, query: TradeoffQuery) -> Tradeoff:
        if not query.metrics:
            return Tradeoff(query.objective, None, 0.0)

        scored = [
            (m, _objective_value(m, query.objective)) for m in query.metrics
        ]
        best = max(scored, key=lambda item: item[1]) if query.higher_is_better else min(
            scored, key=lambda item: item[1]
        )
        values = [v for _, v in scored]
        if max(values) == min(values):
            return Tradeoff(query.objective, None, 0.0)
        margin = round(abs(best[1] - (min(values) if query.higher_is_better else max(values))), 4)
        return Tradeoff(query.objective, best[0].policy, margin)

    def handle_recommendations(self, query: RecommendationQuery) -> list[Recommendation]:
        return recommend(query.metrics, query.objectives)


def _objective_value(metrics: CacheMetrics, objective: Objective) -> float:
    if objective is Objective.HIT_RATE:
        return metrics.hit_rate
    if objective is Objective.MEMORY:
        return float(metrics.peak_entries)
    if objective is Objective.LATENCY:
        return metrics.throughput
    if objective is Objective.SIMPLICITY:
        return SIMPLICITY_SCORE[metrics.policy]
    return 0.0


# Complexity of each policy, on a 3 (simple) to 1 (complex) scale. This is a
# design judgement, not something a benchmark can measure.
SIMPLICITY_SCORE: dict[EvictionPolicy, float] = {
    EvictionPolicy.LRU: 3.0,
    EvictionPolicy.LFU: 2.0,
    EvictionPolicy.ARC: 1.0,
}


def recommend(
    metrics: list[CacheMetrics] | tuple[CacheMetrics, ...],
    objectives: tuple[Objective, ...] = (
        Objective.HIT_RATE,
        Objective.MEMORY,
        Objective.SIMPLICITY,
    ),
) -> list[Recommendation]:
    """Decision guide: the best policy per objective, with its measured value."""
    if not metrics:
        return []

    higher_is_better = {
        Objective.HIT_RATE: True,
        Objective.LATENCY: True,
        Objective.SIMPLICITY: True,
        Objective.MEMORY: False,  # a smaller footprint is better
    }
    rationales = {
        Objective.HIT_RATE: "serves the most lookups from cache",
        Objective.MEMORY: "keeps the smallest working set",
        Objective.LATENCY: "delivers the highest throughput",
        Objective.SIMPLICITY: "is the simplest to implement and reason about",
    }

    guide: list[Recommendation] = []
    for objective in objectives:
        scored = [(m, _objective_value(m, objective)) for m in metrics]
        pick = (
            max(scored, key=lambda item: item[1])
            if higher_is_better[objective]
            else min(scored, key=lambda item: item[1])
        )
        guide.append(
            Recommendation(
                objective=objective,
                policy=pick[0].policy,
                rationale=rationales[objective],
                measured=pick[1],
            )
        )
    return guide


# =============================================================================
# Facade
# =============================================================================

class ConflictingObjectives:
    """Main facade: benchmark policies and analyse the tradeoffs."""

    _repository: InMemoryBenchmarkRepository
    _command_handler: BenchmarkCommandHandler
    _query_handler: TradeoffQueryHandler

    def __init__(self, capacity: int = 3) -> None:
        self.capacity = capacity
        self._repository = InMemoryBenchmarkRepository()
        self._command_handler = BenchmarkCommandHandler(self._repository)
        self._query_handler = TradeoffQueryHandler(self._repository)

    # Commands
    def benchmark(
        self,
        accesses: list[str],
        policies: tuple[EvictionPolicy, ...] = (
            EvictionPolicy.LRU,
            EvictionPolicy.LFU,
            EvictionPolicy.ARC,
        ),
        store: bool = True,
    ) -> list[CacheMetrics]:
        return self._command_handler.handle_benchmark(
            BenchmarkCommand(
                accesses=accesses,
                capacity=self.capacity,
                policies=policies,
                store=store,
            )
        )

    # Queries
    def analyse(self, accesses: list[str]) -> dict[EvictionPolicy, CacheMetrics]:
        """Benchmark the default policies and return one metrics object each."""
        return {m.policy: m for m in self.benchmark(accesses, store=False)}

    def tradeoffs(self, accesses: list[str]) -> list[Tradeoff]:
        """One tradeoff verdict per objective, from the same access pattern."""
        metrics = self.benchmark(accesses, store=True)
        return [
            self._query_handler.handle_tradeoff(TradeoffQuery(obj, tuple(metrics)))
            for obj in (
                Objective.HIT_RATE,
                Objective.MEMORY,
                Objective.LATENCY,
                Objective.SIMPLICITY,
            )
        ]

    def recommendations(self, accesses: list[str]) -> list[Recommendation]:
        """Decision guide for the measured access pattern."""
        return self._query_handler.handle_recommendations(
            RecommendationQuery(tuple(self.benchmark(accesses, store=True)))
        )


# =============================================================================
# Functional interface
# =============================================================================

def _replay(cache: Cache, accesses: list[str]) -> None:
    """Replay a trace as a user would: look the key up, store it on a miss."""
    for key in accesses:
        if cache.get(key) is None:
            cache.put(key, key.upper())


def simulate(
    accesses: list[str],
    capacity: int = 3,
    policy: EvictionPolicy = EvictionPolicy.LRU,
) -> CacheMetrics:
    """Run one policy over an access pattern and return its metrics."""
    cache = Cache(capacity=capacity, policy=policy)
    _replay(cache, accesses)
    return cache.metrics


def compare(
    accesses: list[str],
    capacity: int = 3,
    policies: tuple[EvictionPolicy, ...] = (
        EvictionPolicy.LRU,
        EvictionPolicy.LFU,
        EvictionPolicy.ARC,
    ),
) -> dict[EvictionPolicy, CacheMetrics]:
    """Run several policies over the same access pattern."""
    return {p: simulate(accesses, capacity, p) for p in policies}


def best_policy(
    accesses: list[str], capacity: int = 3, objective: Objective = Objective.HIT_RATE
) -> EvictionPolicy | None:
    """Which policy measures best for an objective on this access pattern."""
    guide = recommend(list(compare(accesses, capacity).values()), (objective,))
    return guide[0].policy if guide else None


def analyze_tradeoffs(
    options: list[dict[str, Any]], capacity: int = 3
) -> dict[str, Any]:
    """Benchmark plain-dictionary options and return a summary report."""
    metrics: list[CacheMetrics] = []
    for option in options:
        policy = option["policy"]
        if isinstance(policy, str):
            policy = EvictionPolicy(policy)
        metrics.append(
            simulate(
                list(option["accesses"]),
                int(option.get("capacity", capacity)),
                policy,
            )
        )

    return {
        "metrics": {m.policy: m for m in metrics},
        "tradeoffs": [
            _tradeoff_report(obj, metrics)
            for obj in (
                Objective.HIT_RATE,
                Objective.MEMORY,
                Objective.LATENCY,
                Objective.SIMPLICITY,
            )
        ],
        "recommendations": recommend(metrics),
    }


def _tradeoff_report(
    objective: Objective, metrics: list[CacheMetrics]
) -> dict[str, Any]:
    query_handler = TradeoffQueryHandler(InMemoryBenchmarkRepository())
    verdict = query_handler.handle_tradeoff(TradeoffQuery(objective, tuple(metrics)))
    return {
        "objective": objective.value,
        "winner": verdict.winner.value if verdict.winner else None,
        "margin": verdict.margin,
        "tie": verdict.is_tie,
    }


# =============================================================================
# Example Usage & Demo
# =============================================================================

if __name__ == "__main__":
    print("=== Kata08: Conflicting Objectives - Demo ===\n")

    # A hot pair of keys, warmed up, then buried under a long one-shot scan.
    # This is where frequency-aware policies earn their keep.
    bursty = ["h0", "h1"] * 5 + [f"scan{i}" for i in range(20)] + ["h0", "h1"] * 5

    # The same hot pair, but interleaved with the scan rather than buried.
    interleaved = [k for i in range(30) for k in ("h0", "h1", f"scan{i}")]

    engine = ConflictingObjectives(capacity=3)

    print("Bursty workload (hot pair buried by a scan, capacity 3):")
    for policy, metrics in engine.analyse(bursty).items():
        print(
            f"  {policy.value.upper():4} hits={metrics.hits:3} misses={metrics.misses:3} "
            f"evictions={metrics.evictions:3} hit_rate={metrics.hit_rate:.2%}"
        )

    print("\nTradeoffs on that workload:")
    for tradeoff in engine.tradeoffs(bursty):
        if tradeoff.winner is None:
            print(f"  {tradeoff.objective.value:10} tie")
        else:
            print(
                f"  {tradeoff.objective.value:10} winner={tradeoff.winner.value.upper():4}"
                f" margin={tradeoff.margin:g}"
            )

    print("\nDecision guide on that workload:")
    for rec in engine.recommendations(bursty):
        print(f"  {rec.objective.value:10} -> {rec.policy.value.upper():4} ({rec.rationale})")

    print("\nSame access pattern, scan interleaved instead of buried:")
    for policy, metrics in compare(interleaved, capacity=3).items():
        print(f"  {policy.value.upper():4} hit_rate={metrics.hit_rate:.2%}")
    print("  Every policy scores about the same here, so there is nothing to")
    print("  choose between them - and no policy is best on every workload.")

    print("\nSequential workload (every key touched once, no reuse at all):")
    for policy, metrics in compare([f"s{i}" for i in range(30)], capacity=3).items():
        print(f"  {policy.value.upper():4} hit_rate={metrics.hit_rate:.2%}")

    print("\nPlain-dictionary functional interface:")
    report = analyze_tradeoffs(
        [
            {"policy": "lru", "accesses": bursty, "capacity": 3},
            {"policy": "lfu", "accesses": bursty},
        ],
        capacity=3,
    )
    for entry in report["recommendations"]:
        print(f"  {entry.objective.value:10} -> {entry.policy.value.upper()}")
