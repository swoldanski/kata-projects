# kata-projects

A curated collection of code katas for practice and learning, organized into four themed collections:

| Collection | Katas | Focus |
|------------|-------|-------|
| **Dave Thomas CodeKata** | 21 | Classic programming exercises (algorithms, modeling, design) |
| **Gaurav Arora TDD Katas** | 16 | Test-driven development classics (String Calculator, Bowling, Game of Life, etc.) |
| **Wonderland Clojure Katas** | 7 | Lewis Carroll-themed puzzles (ciphers, word ladders, river crossing, mazes) |
| **SensioLabs PoleDev Katas** | 5 | Symfony/form-focused exercises (data transformers, events, file upload, translations) |

**Total: 49 katas** — each in its own directory with a detailed `README.md` describing the problem, requirements, examples, and suggested TDD steps.

## Purpose

This repository serves as a **kata catalog and practice workspace**. Each kata is a self-contained exercise you can implement in any language. The structure follows the aSDLC framework for project governance.

## Structure

```
kata-projects/
├── AGENTS.md                    # aSDLC rail (binding contract)
├── ROADMAP.md                   # Project direction
├── CHANGELOG.md                 # Notable changes
├── CONTRIBUTING.md              # Contribution workflow
├── LICENSE                      # CC0 (public domain)
├── pyproject.toml               # Python project config (uv)
├── docs/                        # User manual (how to practice katas)
├── architecture/                # DevSecOps manual (internal design)
├── tests/                       # Verification mechanisms
├── dave-thomas-codekata/        # 21 katas from codekata.com
├── gaurav-arora-tdd-katas/      # 16 TDD katas
├── wonderland-clojure-katas/    # 7 Wonderland-themed katas
└── sensiolabs-poledev-katas/    # 5 Symfony-style katas
```

## Quick Start

```bash
# Install Python tooling (uv)
uv sync

# Run tests
uv run pytest

# Pick a kata and start coding!
cd dave-thomas-codekata/kata02-karate-chop
# Implement chop() in your language of choice
```

## Kata Format

Each kata directory contains:
- `README.md` — Problem statement, rules, examples, TDD steps, extensions
- (You add) Implementation files in your preferred language

## License

CC0 (Public Domain) — see [LICENSE](LICENSE)