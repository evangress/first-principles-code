<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Evan Gress -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A teaching template: a Python script + class library meant to functionally teach engineers Python techniques and empower them to solve real-world engineering problems. Because it's a teaching artifact, code clarity, docstrings, and explanatory comments are first-class deliverables — not afterthoughts. See "Authoring conventions" below.

The full project design — intended `main.py` demo, the per-domain library classes, and the README deliverables — lives in [SPEC.md](SPEC.md). Read it before implementing features.

## Current state vs. intended design

The repo is scaffolded but largely unimplemented. Know the difference before you start:

- `main.py` — currently PyCharm hello-world boilerplate. **Intended (SPEC):** a demo that calculates displacement from a known acceleration and velocity as a function of time (using `math` / `scipy`).
- `library/` — empty except an `__include__` marker file. **Intended (SPEC):** one class per engineering domain.
- `pyproject.toml` — `dependencies = []`. Add `scipy` (and likely `numpy`) here when implementing the `main.py` demo and the math-heavy classes.
- No README, no tests yet — both are intended deliverables.

## Tooling & commands

Python **3.14+**, managed with **uv** (a `.venv` already exists).

```bash
uv sync                  # install deps from pyproject.toml into .venv
uv add scipy numpy       # add a dependency (edits pyproject.toml + lockfile)
uv run main.py           # run the main script
uv run python -c "..."   # run arbitrary python in the project env
```

There is no test runner or linter configured yet. If you add tests, prefer `pytest` (`uv add --dev pytest`, run with `uv run pytest`, single test via `uv run pytest path::test_name`).

## Library architecture

`./library` holds one class per engineering domain, each class grouping related calculation methods (see SPEC.md for the full planned class list). When adding domains beyond that list, follow the same one-class-per-file, domain-grouped pattern.

## Authoring conventions

These exist to make the code itself a teaching tool — follow them in all new code:

- Use `**kwargs` for method/function parameters to demonstrate verbose, explicit variable passing.
- Every class and method gets a docstring — they double as documentation examples.
- Comment significant code sections explaining the *why*, not just the *what*.
