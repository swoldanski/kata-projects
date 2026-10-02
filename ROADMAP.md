# Roadmap

A short explanation of this file's purpose: it records the project's
direction (vision, what is built, what is planned, and what is
explicitly out of scope) so contributors can keep edits aligned with
intent. It is a direction aid, not a contract — `AGENTS.md` remains the
binding rules.

## Vision

**kata-projects** is a curated collection of 49 code katas organized into four themed collections, providing a structured workspace for deliberate programming practice. Each kata is a self-contained exercise with a detailed problem statement, requirements, examples, and suggested TDD progression — ready to implement in any language.

## Guidelines for the three lists

- **Implemented** — shipped and live in this repo; cross out replaced or removed one.
- **Backlog** — agreed future work, not yet started.
- **Not in scope** — explicitly excluded on purpose, to prevent drift; list only deliberate exclusions, not mere omissions.
- Keep each item one concise line; link issues/PRs/docs where they exist.

## Implemented

- Four kata collections scaffolded with 49 total katas:
  - Dave Thomas CodeKata (21 katas from codekata.com)
  - Gaurav Arora TDD Katas (16 katas from TDD-Katas collection)
  - Wonderland Clojure Katas (7 katas from wonderland-clojure-katas)
  - SensioLabs PoleDev Katas (5 katas from devdrops/Katas)
- Each kata has a `README.md` with problem statement, rules, examples, TDD steps, extensions
- aSDLC framework installed as governance (AGENTS.md, ROADMAP.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE)
- Repository structure follows aSDLC: `/docs` (user manual), `/architecture` (DevSecOps), `/tests` (verification)
- **Python starter templates** for all 49 katas (DDD/CQRS/Repository + in-memory, with failing tests)
- **User manual** (`docs/README.md`) — kata selection, TDD workflow, language setup, collections overview
- **DevSecOps manual** (`architecture/README.md`) — repo structure, aSDLC, testing philosophy, tooling, templates, release
- **Enhanced verification** (`tests/test_catalog.py` — 8 tests: structure, templates, README format, duplicates)
- **Kata01: Supermarket Pricing** — Python implementation with DDD/CQRS/Repository patterns, 36 tests passing
- **Kata02: Karate Chop** — 5 unique binary search implementations (iterative, recursive, functional, built-in, tail-recursive), 47 tests passing
- **Kata03: How Big? How Fast?** — Estimation calculator for bits, storage, time with 32 tests passing
- **Kata04: Data Munging** — Weather/soccer data parsing with DRY fusion, 32 tests passing
- **Kata05: Bloom Filters** — Probabilistic set membership with MD5/SHA256/FNV/double hashing, 43 tests passing
- **Kata06: Anagrams** — Anagram grouping with four signature strategies (sorted/prime/count/counter), 20 tests passing
- **Kata07: How'd I Do?** — Quiz scoring with five question types, partial credit, weighted and bonus questions, reports and grading scales, 32 tests passing

## Backlog

- Kata08: Conflicting Objectives - Python implementation
- Kata09: Back to the Checkout - Python implementation
- Kata10: Hashes vs. Classes - Python implementation
- Kata11: Sorting It Out - Python implementation
- Kata12: Best Sellers - Python implementation
- Kata13: Counting Code Lines - Python implementation
- Kata14: Tom Swift Under the Milkwood - Python implementation
- Kata15: A Diversion - Python implementation
- Kata16: Business Rules - Python implementation
- Kata17: More Business Rules - Python implementation
- Kata18: Transitive Dependencies - Python implementation
- Kata19: Word Chains - Python implementation
- Kata20: Klondike - Python implementation
- Kata21: Simple Lists - Python implementation
- String Sum Kata - Python implementation
- String Calculator Kata (via Roy Osherove) - Python implementation
- The Bowling Game Kata (via Uncle Bob) - Python implementation
- FizzBuzz Kata - Python implementation
- OddEven Kata - Python implementation
- Prime Factor Kata (via Uncle Bob) - Python implementation
- Game of Life - Python implementation
- Harry Potter Kata - Python implementation
- LCD Digits Kata - Python implementation
- Leap Year Kata - Python implementation
- Mine Fields Kata - Python implementation
- Poker Hands Kata - Python implementation
- Recently Used List Kata - Python implementation
- Reversi (Othello) Kata - Python implementation
- Yahtzee Kata - Python implementation
- Word Wrap Kata - Python implementation
- Alphabet Cipher - Python implementation
- Card Game War - Python implementation
- Doublets - Python implementation
- Fox, Goose, Bag of Corn - Python implementation
- Magic Square - Python implementation
- Tiny Maze - Python implementation
- Wonderland Number - Python implementation
- Kata 1: Data Transformer - Python implementation
- Kata 2: Event Listener / Event Dispatcher - Python implementation
- Kata 3: Inherit Data / Virtual Form - Python implementation
- Kata 4: File Upload - Python implementation
- Kata 5: Manage Translations - Python implementation

## Not in scope

- Hosting a web-based kata platform or runner
- Automated code evaluation/grading
- Community features (leaderboards, comments, solutions gallery)
- Non-kata programming exercises (full projects, tutorials, courses)
- **GitHub Actions CI** — prefer local `uv run pytest` + pre-commit; CI adds maintenance without proportional value for a personal practice repo
- **Language-specific templates** — katas are language-agnostic by design; adding templates per language creates drift and maintenance burden
- **Machine-readable kata metadata index** — YAML/JSON index adds schema overhead; human-readable README.md is the source of truth