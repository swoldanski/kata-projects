## [Unreleased]

## [0.3.8] - 2026-10-02

### Added
- **Kata08: Conflicting Objectives** — Cache eviction strategies benchmarked against each other:
  - Three interchangeable policies behind one `EvictionStrategy` protocol: LRU (recency log), LFU (per-key counts) and ARC (adaptive between the two)
  - `Cache` aggregate that delegates eviction to the injected strategy, with capacities, hit/miss counting and eviction tracking
  - A benchmark replaying an access trace as a user would (look up, store on a miss) and measuring hit rate, misses, evictions and throughput
  - `Tradeoff` verdicts and a `Recommendation` decision guide showing that no policy is best everywhere: on the bursty trace LFU/ARC reach 45% against LRU's 40%, while on an interleaved trace all three tie
  - Full DDD/CQRS/Repository architecture with `InMemoryBenchmarkRepository`
  - Functional interface (`simulate`, `compare`, `best_policy`, `analyze_tradeoffs`)
  - 41 tests covering policy behaviour, metrics, tradeoff analysis, architecture and long traces

### Changed
- Repository-wide hygiene baseline: `ruff check .` and `mypy .` now pass across all 100 source files
  - Fixed the documented-but-broken lint invocation (`ruff .` → `ruff check .`) everywhere it appeared
  - Migrated the deprecated top-level ruff settings into `[tool.ruff.lint]`
  - Fixed two latent bugs found by the checkers: `Money.__mul__` now accepts `Decimal` weight quantities, and `find_min_spread_generic` calls the real `parse_lines` parser method

## [0.3.7] - 2026-10-02

### Added
- **Kata07: How'd I Do?** — Quiz scoring system:
  - Five question types: multiple choice, true/false, short answer, numeric range, bonus
  - Answer matching rules: case-sensitive by default, optional case-insensitive matching for short answers, partial credit for answers containing the key
  - Numeric-range questions scale credit by closeness inside the interval
  - Weighted questions and bonus questions that add points on top of the base total
  - `ScoreReport` aggregate with per-question `QuestionResult`s and a detailed report listing every question not fully correct
  - Grading scales: percentage, letter grade (customisable boundaries) and 4.0 GPA
  - Full DDD/CQRS/Repository architecture with `InMemoryQuizRepository`
  - Functional interface (`score_quiz`, `score_percentage`, `letter_grade`, `build_quiz`)
  - 32 tests covering question types, scoring rules, grading scales, architecture and large-quiz scale

## [0.3.6] - 2026-10-02

### Added
- **Kata06: Anagrams** — Group words into anagram sets:
  - Four interchangeable signature strategies: sorted letters, prime factorization, 26-slot letter counts, frozen Counter
  - `AnagramGroup` aggregate with size, word length, membership and anagram-set checks
  - Find anagrams of a word, largest group, longest group, and dictionary statistics
  - Full DDD/CQRS/Repository architecture with `InMemoryAnagramRepository`
  - Functional interface (`group_anagrams`, `find_anagram_sets`, `largest_anagram_group`, `timed_group`)
  - 20 tests covering grouping, strategies, aggregates, filtering, statistics and scale

## [0.3.5] - 2026-10-02

### Added
- **Kata05: Bloom Filters** — Probabilistic set membership with tunable false-positive rate:
  - `BloomFilterConfig` computing optimal bit-array size `m` and hash count `k` from desired n and p
  - Hash functions: MD5, SHA256, FNV-1a, and double hashing (`h_i(x) = (h1(x) + i·h2(x)) mod m`)
  - Full DDD/CQRS/Repository architecture with `InMemoryBloomFilterRepository`
  - Statistics: elements added, estimated false-positive rate, fill ratio
  - Functional interface with `create_bloom_filter(n, p)` factory, `in` operator, multi-item ops
  - 43 comprehensive tests covering config, hashing, membership, statistics, and architecture patterns

## [0.3.4] - 2026-10-02

### Added
- **Kata04: Data Munging** — Weather/soccer data parsing with DRY fusion:
  - Part One: Weather data parsing (min temperature spread)
  - Part Two: Soccer data parsing (min goal difference)
  - Part Three: DRY fusion with shared ColumnParser and generic min-finder
  - Full DDD/CQRS/Repository architecture with LocalFileRepository
  - 32 comprehensive tests covering parsing, DRY fusion, and architecture patterns
  - Functional and class-based interfaces

## [0.3.3] - 2026-10-02

### Added
- **Kata03: How Big? How Fast?** — Estimation calculator for bits, storage, time:
  - Bits estimation for unsigned integers (log2 ceiling)
  - Storage: town records (chars per record), binary tree (32/64-bit with pointer overhead)
  - Time: modem transfer (baud rate), binary search scaling (logarithmic), password cracking (combinatorial)
  - Full DDD/CQRS/Repository architecture with estimation history tracking
  - 32 comprehensive tests covering all estimation categories and architecture patterns
  - Functional and class-based interfaces

## [0.3.2] - 2026-10-02

### Added
- **Kata02: Karate Chop** — 5 unique binary search implementations:
  - Iterative (traditional low/high pointers)
  - Recursive (divide and conquer)
  - Functional (array slices with offset tracking)
  - Built-in (Python's bisect module)
  - Tail-recursive (recursive call as last operation)
  - Full DDD/CQRS/Repository architecture with search history tracking
  - 47 comprehensive tests covering all algorithms, edge cases, TDD progression
  - Search history tracking and statistics per algorithm

## [0.3.1] - 2026-10-02

### Added
- **Kata01: Supermarket Pricing** — Full Python implementation following DDD/CQRS/Repository patterns with in-memory state
  - Value Objects: `Money` (Decimal with rounding), `Quantity` (with units)
  - Entities: `Product` (aggregate root), `PricingRule` (value object)
  - Repository: `InMemoryProductRepository` (dict-based, no external persistence)
  - Domain Service: `PricingService` (price calculation logic)
  - CQRS: `ProductCommandHandler` (writes) + `ProductQueryHandler` (reads)
  - Facade: `PricingEngine` (main entry point)
  - Four pricing types: Simple, Volume (N for $X), Weight ($X/lb), Buy N Get M Free
  - 36 comprehensive tests covering all pricing scenarios, edge cases, and architecture patterns
  - Design document function: `design_pricing_model()`

## [0.3.0] - 2026-10-02

### Added
- **Backlog populated** — All 49 katas added to ROADMAP.md backlog with proper names from README.md titles (e.g., "Kata01: Supermarket Pricing", "String Calculator Kata (via Roy Osherove)", "Alphabet Cipher", "Kata 1: Data Transformer")
- **Kata names standardized** — Backlog entries now match exact `# ` headings from each kata's README.md

## [0.2.0] - 2026-10-02

### Added
- **User Manual** (`docs/README.md`) — How to pick katas, TDD workflow, language setup, collections overview
- **DevSecOps Manual** (`architecture/README.md`) — Repository structure, aSDLC governance, testing philosophy, Python tooling, template generation, release process
- **Enhanced Catalog Tests** (`tests/test_catalog.py`) — 8 tests: structure, templates, README format consistency
- **Code Examples** — All 49 kata READMEs now have `## Examples` with runnable Python snippets
- **Python starter templates** for all 49 katas (DDD/CQRS/Repository + in-memory, with failing tests)
- **Backlog completed** — All 4 original backlog items implemented and verified

## [0.1.0] - 2026-10-02

### Added
- **Implementation Preferences** in `AGENTS.md` — DDD, CQRS, Repository pattern, and in-memory state as preferred architectural patterns for kata solutions contributed to this repository.
- Four kata collections scaffolded with 49 total katas:
  - Dave Thomas CodeKata (21 katas)
  - Gaurav Arora TDD Katas (16 katas)
  - Wonderland Clojure Katas (7 katas)
  - SensioLabs PoleDev Katas (5 katas)
- aSDLC framework baseline (AGENTS.md, ROADMAP.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE)
- Python tooling via uv (pytest, ruff, mypy)
- Catalog verification tests (5 tests passing)
- Repository structure following aSDLC conventions