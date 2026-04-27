# Toga - Agent Development Guide

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure, shell commands, and other important information, read the current plan
<!-- SPECKIT END -->

This file tells autonomous coding agents (and human contributors using agent tools) how to be productive in this repository without breaking it. It is operational guidance; the binding rules live in `.specify/memory/constitution.md` and the contribution docs under `docs/en/how-to/contribute/`. When this file disagrees with either, the constitution wins.

## What Toga is

Toga is a Python-native, OS-native GUI toolkit published under BSD-3-Clause as part of the BeeWare suite. A single `toga-core` API is rendered by a platform-specific backend so that one Python codebase produces native apps on macOS, Windows, Linux, iOS, Android, Web, and terminal.

## Repository layout

| Path | What it contains |
| --- | --- |
| `core/` | `toga-core` — the public API and shared widget contracts. |
| `travertino/` | Style and layout engine used by `core`. |
| `dummy/` | Reference headless backend; MUST implement the full core API so core tests can run without a GUI. |
| `cocoa/` | macOS backend. |
| `gtk/` | Linux/GTK backend (GTK3 stable, GTK4 experimental). |
| `winforms/` | Windows backend. |
| `iOS/` | iOS backend. |
| `android/` | Android backend. |
| `textual/` | Terminal backend. |
| `web/` | Web backend. |
| `qt/` | Linux/Qt backend. |
| `positron/` | Briefcase plugin for generating apps where the UI has been defined with web tools. Similar to Electron, but using Python for the web server |
| `testbed/` | Briefcase app used to validate backend behaviour on a real platform. |
| `docs/en/` | User and contributor documentation (MkDocs, `mkdocs.en.yml`). |
| `changes/` | Towncrier fragments (`<issue>.<kind>.md`) — one per user-visible change. |
| `examples/`, `demo/` | Standalone sample apps. |
| `.specify/` | SpecKit workflow assets (constitution, templates, extensions). |

Do not create new top-level directories without a clear constitutional reason; extend existing ones.

## Non-negotiables (from the constitution)

1. **Backend parity.** A new `toga-core` API MUST have a concrete implementation plan for every production backend. The Dummy backend MUST always implement the full surface.
2. **Native behaviour.** Production backends MUST delegate to the native toolkit. No emulated/custom-drawn widgets without documented justification.
3. **Comprehensive tests (NON-NEGOTIABLE).** 100% line coverage for `core` and `travertino`. Backend changes MUST be exercised via `testbed/`. Bug fixes MUST include a regression test that fails before the fix.
4. **Documented change.** Every user-visible change MUST include a `changes/<issue>.<kind>.md` fragment and updated docs. Breaking changes require a deprecation release.
5. **Contributor accountability.** The submitter owns the diff, regardless of AI assistance. Follow the BeeWare Code of Conduct and AI Policy.

Any PR failing one of these is rejected, not waived.

## Toolchain

- **Python**: 3.10–3.14 (see `core/pyproject.toml` classifiers).
- **Task runner**: `tox` (with `tox-uv`). Install the dev tooling via `uv pip install --group dev` at the repo root, or let `tox` bootstrap.
- **Lint/format**: `ruff` (check + format), `codespell`, `rumdl` (Markdown), configured in root `pyproject.toml`.
- **Pre-commit**: `pre-commit run --all-files` — MUST pass before PR.
- **Packaging / testbed driver**: `briefcase`.
- **Release notes**: `towncrier` (config in root `pyproject.toml`).
- **Docs**: MkDocs; built with the `docs` dependency group.

Do not replace or bypass these tools. Add new dependencies only with a clear need and a compatible license (BSD-3-Clause friendly).

## Canonical commands

Run from the repository root unless noted.

```console
# Everything pre-commit checks (ruff, format, codespell, rumdl, etc.)
pre-commit run --all-files

# Core + Travertino test suites with coverage (MUST be 100%)
tox -m test

# Just core
tox -m test-core

# Just Travertino
tox -m test-trav

# A single test file against core
tox -e py-cov -- core/tests/path/to/test_file.py

# A single test file against Travertino
tox -e py-trav -- travertino/tests/path/to/test_file.py

# Towncrier draft (preview assembled release notes)
tox -e towncrier-check

# Docs lint
tox -e docs-lint
```

### Testbed (backend validation)

The core suite uses the Dummy backend. Real backend behaviour is validated through the testbed app. Install only the backend under test in your virtualenv, then:

```console
# Desktop (from testbed/)
briefcase dev --app testbed --test

# GTK variants (Linux)
briefcase dev --app testbed --test
TOGA_GTK=4 TOGA_GTKLIB=None briefcase dev --app testbed --test
TOGA_GTK=4 TOGA_GTKLIB=Adw briefcase dev --app testbed --test

# Qt (Linux)
briefcase dev --app testbed-qt --test

# Textual (Linux)
briefcase dev --app testbed-textual --test

# Mobile (requires the relevant SDK/toolchain)
briefcase run android --app testbed --test
briefcase run iOS --app testbed --test   # macOS host only

# Subset with slow mode for visual inspection
briefcase dev --app testbed --test -- tests/widgets/test_button.py --slow
```

**Do not touch the keyboard/mouse while the testbed is running** — it drives input programmatically and will desync.

## Change notes

Every user-visible PR needs a file in `changes/`:

```text
changes/<issue_or_pr_number>.<kind>.md
```

`<kind>` MUST be one of: `feature`, `bugfix`, `removal`, `doc`, `misc`. Content is one or more sentences of past-tense prose describing the user-visible change. `misc` entries are hidden from release notes and appropriate for purely internal changes. Do not edit `docs/en/about/releases.md` directly; towncrier assembles it at release time.

## Coding conventions

- Follow the Toga code style guide linked from `CONTRIBUTING.md`. Ruff enforces most of it; do not disable rules locally.
- Keep public API surface minimal and documented. New public names MUST appear in reference docs under `docs/en/reference/api/`.
- Type hints: use them on public API; keep them consistent with the `.pyi` stub (`core/src/toga/__init__.pyi`) when applicable. That stub is excluded from Ruff — hand-edit it carefully.
- `# pragma: no cover` is reserved for the cases already whitelisted in `tool.coverage.coverage_conditional_plugin.rules`. Do not introduce new ones to work around missing tests.
- `filterwarnings = ["error"]` is set for pytest; warnings in tests are failures. Either fix the root cause or add a scoped, commented `pytest.warns(...)` / `filterwarnings` mark.
- `isort` config in root `pyproject.toml` lists the first-party backend packages; add new packages there if you create one.

## Documentation expectations

- Every new public API, widget, or behavioural change MUST update `docs/en/` in the same PR.
- Tutorials live under `docs/en/tutorial/`, how-tos under `docs/en/how-to/`, reference under `docs/en/reference/`, topic explanations under `docs/en/topics/`.
- Build-time doc linting runs through `tox -e docs-lint`; fix anything it reports.
- Markdown files in this project (including `AGENTS.md`, `docs/en/`, and `changes/` fragments) must **not** use hard line breaks to enforce an 80-character column limit. Each paragraph or list item must be written as a single unbroken line, regardless of its length. Let the reader's editor or renderer handle wrapping. This rule applies to all prose. Code blocks, directory trees, and other pre-formatted blocks are exempt — keep those readable within their own constraints. When writing or editing any `.md` file, do not insert newlines mid-sentence or mid-paragraph to stay within 80 columns.
- Follow the BeeWare documentation style guide (linked from `CONTRIBUTING.md`).

## Pull-request workflow

1. Branch off `main` with a descriptive name. Do not push to `main`.
2. Make the smallest change that addresses one issue. Avoid scope creep; file a separate issue/PR for drive-by refactors.
3. Before opening the PR, run locally:
    - `pre-commit run --all-files`
    - `tox -m test` (expect 100% coverage)
    - Testbed on any backend the change affects
4. Include in the PR:
    - A `changes/<issue>.<kind>.md` fragment
    - Docs updates when user-visible
    - A description naming the issue closed and the backends exercised
5. CI MUST be green. Reviewers confirm the five constitutional principles; failures are fixed, not waived.
6. Default merge strategy is squash; the squash message is what users will read, so make it describe the user-visible change.

## Agent-specific rules

Agents operating in this repo MUST:

- Load `.specify/memory/constitution.md` before any change that affects public API, backends, test coverage, or release tooling.
- Prefer editing existing files over creating new ones. Never proactively create new top-level files or directories.
- Keep the `<!-- SPECKIT START --> ... <!-- SPECKIT END -->` block at the top of this file intact; SpecKit commands inject plan context there.
- Never add `# pragma: no cover`, `# noqa`, or disable Ruff/codespell rules inline to pass CI; diagnose and fix the underlying issue.
- Never commit secrets, API keys, `.env` files, or contributor PII.
- Never rewrite Git history on `main` or force-push shared branches.
- When uncertain about backend parity or API shape, open an issue or discussion before implementing; Toga favours design-first for anything non-trivial (see `docs/en/how-to/contribute/how/propose-feature.md`).
- Disclose AI assistance in the PR description where it is material to review, per the BeeWare AI Policy.

## Where to look next

- `CONTRIBUTING.md` — entry point for all contributors.
- `.specify/memory/constitution.md` — binding project principles.
- `docs/en/how-to/contribute/` — style guides, PR process, review guide, scope-creep guide, AI policy.
- `docs/en/reference/platforms/` — per-backend requirements and status.
- Toga documentation site: <https://toga.beeware.org>
- BeeWare community and Code of Conduct: <https://beeware.org>
