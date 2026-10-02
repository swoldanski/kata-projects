# Contributing

Thank you for contributing to the aSDLC project! Please follow the guidelines below to ensure smooth collaboration and maintain project quality.

## Overview

This project uses the aSDLC framework as defined in [AGENTS.md](AGENTS.md) for structured software development. All contributions are tracked through the following core documents:

- [`AGENTS.md`](AGENTS.md) - Agent contracts and hierarchy
- [`ROADMAP.md`](ROADMAP.md) - Project direction and scope
- [`CHANGELOG.md`](CHANGELOG.md) - Change tracking

## Workflow

### Pre-Work

1. Ensure you have the latest version of the framework documents:

   ```bash
   git pull origin main
   ```

2. Verify the required documents are present and current:
   - [`AGENTS.md`](AGENTS.md) - read before editing
   - [`ROADMAP.md`](ROADMAP.md) - must be kept current per user preferences
   - [`CHANGELOG.md`](CHANGELOG.md) - all notable changes documented

### Branch & Development

1. Create a feature branch from `main`:

   ```bash
   git checkout -b feature/short-description
   ```

2. Make your changes following the project's purpose and scope.

3. If adding a user-facing feature:
   - Create corresponding documentation in `/docs/` (the user manual)
   - Update [`/docs/README.md`](/docs/README.md) if new files/directories are added

4. If documenting contributors or non-end-user implementation details:
   - Add it under `/architecture/` (the DevSecOps manual), not `/docs/`

### Pre-Commit Checks

Before committing, run the verification checks (see [Verification Mechanisms](#verification-mechanisms) below).

### Commit Message Guidelines

Conventional commit format:

```
<type>(<scope>): <description>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### AI Attribution

If you use AI tools to help write code, please note this in your pull request description. Use commit trailers where appropriate:

    Assisted-by: <name of code assistant>
    Generated-by: <name of code assistant>

Per the root `AGENTS.md` User Preferences, all notable AI-assisted changes must be documented for transparency and traceability.

### Pull Request Process

1. Push your branch and open a PR against `main`
2. Ensure all verification checks pass (see below)
3. Fill the PR template describing:
   - What changed and why
   - Which aSDLC pass this aligns with
   - Any breaking changes
   - Testing performed

### Post-Merge

After PR merge:
- Branch can be deleted

## Code of Conduct

Be respectful and constructive in all interactions. Follow the project's aSDLC pass closeout procedure for any changes affecting structure, contracts, or workflows.

## Verification Mechanisms

This project uses the following verification checks (defined in `tests/AGENTS.md`):

- **Catalog tests**: `uv run pytest tests/ -v`
  - Validates kata structure, README format, template files, no duplicates
- **Kata tests**: `uv run pytest <collection>/<kata>/ -v`
  - Behavioral tests for each implemented kata
- **Lint**: `uv run ruff check .`
- **Type check**: `uv run mypy .`

Before committing, run all verification:
```bash
uv run pytest tests/ -v
uv run pytest dave-thomas-codekata/ gaurav-arora-tdd-katas/ wonderland-clojure-katas/ sensiolabs-poledev-katas/ -v
uv run ruff check .
uv run mypy .
```

---
 
Questions? Open an issue or reach out to the maintainers.