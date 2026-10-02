# DevSecOps Manual

Internal documentation for contributors — how the repository works under the hood.

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [aSDLC Governance](#asdlc-governance)
3. [Testing Philosophy](#testing-philosophy)
4. [Python Tooling](#python-tooling)
5. [Kata Template Generation](#kata-template-generation)
6. [Release Process](#release-process)

---

## Repository Structure

```
kata-projects/
├── AGENTS.md                    # aSDLC rail (binding contract)
├── ROADMAP.md                   # Project direction (vision/backlog/scope)
├── CHANGELOG.md                 # Keep a Changelog format
├── CONTRIBUTING.md              # Contribution workflow
├── LICENSE                      # CC0-1.0 (public domain)
├── pyproject.toml               # Python config (uv, pytest, ruff, mypy)
├── README.md                    # Project overview
├── generate_templates.py        # Kata template generator
├── docs/                        # User manual (how to practice)
│   ├── AGENTS.md                # docs governance
│   └── README.md                # User-facing documentation
├── architecture/                # DevSecOps manual (this directory)
│   ├── AGENTS.md                # architecture governance
│   └── README.md                # This file
├── tests/                       # Verification mechanisms
│   ├── AGENTS.md                # tests governance
│   ├── README.md                # Test suite overview
│   └── test_catalog.py          # Catalog structure validation
├── dave-thomas-codekata/        # 21 katas from codekata.com
├── gaurav-arora-tdd-katas/      # 16 TDD katas
├── wonderland-clojure-katas/    # 7 Wonderland katas
└── sensiolabs-poledev-katas/    # 5 SensioLabs katas
```

### Directory Purposes

| Directory | Purpose | Audience |
|-----------|---------|----------|
| `/docs` | User manual — how to practice katas | End users (practitioners) |
| `/architecture` | DevSecOps — how repo works internally | Contributors |
| `/tests` | Verification — catalog integrity | CI / Contributors |
| Collection dirs | Kata exercises with templates | Practitioners |

---

## aSDLC Governance

This repository follows the **aSDLC framework** (Agentic SDLC) — a binding `AGENTS.md` hierarchy.

### Core Principles

1. **AGENTS.md files are binding contracts** for their subtrees
2. **Read Before Editing** — Read root AGENTS.md, walk path, read all AGENTS.md along route
3. **Update After Editing** — Update nearest owning AGENTS.md when contracts change
4. **Closeout Required** — Every meaningful change requires closeout pass

### The aSDLC Pass

```
Read Before Editing → Edit → Update After Editing → Closeout
```

### Closeout Checklist (from root AGENTS.md)

1. Re-check changed paths against aSDLC chain
2. Update nearest owning docs and affected parents/children
3. Refresh every affected Child aSDLC Index
4. Remove stale or contradictory text
5. Run existing verification (`uv run pytest tests/`)
6. Report any docs intentionally left unchanged and why

### Hierarchy

```
Root AGENTS.md (aSDLC rail)
├── /docs/AGENTS.md → owns /docs
├── /architecture/AGENTS.md → owns /architecture
├── /tests/AGENTS.md → owns /tests
└── Collection dirs → no AGENTS.md (governed by root)
```

---

## Testing Philosophy

### Behavioral Testing Only

Per AGENTS.md User Preferences:
> **Testing must follow behavioral philosophy and cost-benefit analysis.**
> Behavior tests guard user-visible functionality across refactoring and remain readable; implementation tests break when code changes and provide no guard.

### What We Test

| Test | Scope | Purpose |
|------|-------|---------|
| `test_catalog.py` | Catalog structure | Verify 49 katas exist, have READMEs, no duplicates |
| Kata tests (generated) | Kata behavior | TDD-driven implementation verification |

### What We DON'T Test

- Implementation details (private methods, call counts)
- Internal structure of generated templates
- Code coverage targets
- Performance benchmarks

### Test Organization

```
tests/
└── test_catalog.py          # Catalog integrity (5 tests)
    ├── test_all_collections_exist
    ├── test_each_kata_has_readme
    ├── test_readme_has_required_sections
    ├── test_no_duplicate_kata_names
    └── test_kata_count_matches_expected

<collection>/<kata>/
└── test_<name>.py           # Kata behavior (3 tests each)
    ├── test_basic_case
    ├── test_edge_cases
    └── test_tdd_progression
```

### Running Tests

```bash
# All catalog tests
uv run pytest tests/ -v

# Single kata tests
uv run pytest dave-thomas-codekata/kata02-karate-chop/test_kata02_karate_chop.py -v

# All kata tests (will fail until implemented)
uv run pytest dave-thomas-codekata/ gaurav-arora-tdd-katas/ wonderland-clojure-katas/ sensiolabs-poledev-katas/ -v
```

---

## Python Tooling

### uv (Package Manager)

```bash
uv sync                    # Install dependencies from uv.lock
uv add pytest              # Add dependency
uv add --dev ruff          # Add dev dependency
uv run pytest              # Run with project environment
uv run python script.py    # Run script with project environment
```

### Configured Tools (pyproject.toml)

| Tool | Purpose | Config |
|------|---------|--------|
| `pytest` | Testing | `testpaths = ["tests"]` |
| `ruff` | Linting | Line length 100, Python 3.12 |
| `mypy` | Type checking | Warn on `Any`, unused ignores |

### Version Management

- Python version pinned via `.python-version` (if present) or `requires-python` in `pyproject.toml`
- Dependencies locked in `uv.lock`
- No virtualenv in repo (created by uv in `.venv/`)

---

## Kata Template Generation

### Generator: `generate_templates.py`

Generates implementation + test files for all 49 katas from a single specification.

### Running the Generator

```bash
python3.12 generate_templates.py
```

### Template Structure

Each kata gets:

```
<kata_dir>/
├── <module_name>.py          # Implementation template
│   ├── Class-based (DDD/CQRS)
│   └── Functional alternative
└── test_<module_name>.py     # Test template
    ├── test_basic_case
    ├── test_edge_cases
    └── test_tdd_progression
```

### Design Principles

1. **DDD/CQRS/Repository ready** — Class structure with commands/queries separation
2. **In-memory only** — No DB, ORM, or external persistence imports
3. **Type hints** — Full type annotations for main functions
4. **NotImplementedError** — Forces TDD implementation
5. **Single specification** — All kata metadata in one Python list

### Adding a New Kata to Generator

Add entry to `KATAS` list in `generate_templates.py`:

```python
("collection/kata-dir", "Description", "main_function", "params", "return_type", "docstring", "ClassName")
```

Then regenerate: `python3.12 generate_templates.py`

---

## Release Process

### Versioning

Follows [Keep a Changelog](https://keepachangelog.com) + SemVer.

### Changelog Format

```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- Feature description

### Changed
- Change description

### Fixed
- Fix description
```

### Release Steps

1. **Accumulate changes** in `[Unreleased]` section
2. **Verify** — `uv run pytest tests/` passes
3. **Promote** — Move `[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`
4. **Tag** — `git tag vX.Y.Z` (when git initialized)
5. **Repeat** — New `[Unreleased]` section for next cycle

### Current Version

**v0.3.7** — Latest release; katas 01-07 implemented on the aSDLC baseline (v0.1.0 scaffolded all 49 katas and templates)

---

## Security

- **No secrets in repo** — `.env` files gitignored
- **No external dependencies** for kata implementations (stdlib only)
- **No network calls** in tests or templates
- **CC0 License** — Public domain, no attribution required

---

## Maintenance

### Regular Tasks

| Task | Frequency | Command |
|------|-----------|---------|
| Update dependencies | Monthly | `uv sync --upgrade` |
| Run all tests | Before commit | `uv run pytest tests/` |
| Lint | Before commit | `uv run ruff check .` |
| Type check | Before commit | `uv run mypy .` |
| Regenerate templates | After adding katas | `python3.12 generate_templates.py` |

### Adding a Kata Collection

1. Create directory under root
2. Add kata subdirectories with READMEs
3. Add entries to `generate_templates.py` KATAS list
4. Run generator
5. Update `tests/test_catalog.py` expected counts
6. Update `ROADMAP.md` Implemented section
7. Add CHANGELOG entry
8. Closeout per aSDLC