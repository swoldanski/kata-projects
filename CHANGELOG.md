## [Unreleased]

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