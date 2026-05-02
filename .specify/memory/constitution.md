<!--
Sync Impact Report
==================
Version change: (uninitialized template) → 1.0.0
Rationale: First ratified constitution. MAJOR bump from unfilled template to a
concrete, enforceable v1.0.0 governance document is appropriate because all
principle slots transition from placeholder to binding text.

Modified principles:
- [PRINCIPLE_1_NAME] → I. Cross-Platform Backend Parity
- [PRINCIPLE_2_NAME] → II. Native Look, Feel, and Behavior
- [PRINCIPLE_3_NAME] → III. Comprehensive Automated Testing (NON-NEGOTIABLE)
- [PRINCIPLE_4_NAME] → IV. Public API Stability and Documented Change
- [PRINCIPLE_5_NAME] → V. Contributor Accountability

Added sections:
- Additional Constraints (supported platforms, toolchain, style, licensing)
- Development Workflow (branching, change notes, PR review, release)
- Governance (amendment, versioning, compliance)

Removed sections: None (template placeholders replaced in place).

Templates requiring updates:
- ✅ .specify/templates/plan-template.md — Constitution Check gate retained;
  principles now concrete so gate can evaluate against named principles.
- ✅ .specify/templates/spec-template.md — No change required; mandatory
  sections already align with constitution (user scenarios, requirements,
  success criteria).
- ✅ .specify/templates/tasks-template.md — Tests remain "optional in the
  template" but Principle III requires tests for Toga code changes; plan/tasks
  output for this repo must include test tasks even when the generic template
  marks them optional. No file edit required; enforced at plan/tasks time.
- ✅ AGENTS.md — Continues to point agents at the current plan; no edit
  required. Agents MUST consult this constitution when a feature affects
  public API, backends, or test coverage.
- ⚠ .specify/templates/constitution-template.md — Left untouched (it is the
  bootstrap template, not the project constitution); no propagation needed.

Follow-up TODOs: None.
-->

# Toga Constitution

Toga is a Python native, OS native GUI toolkit published under the BSD-3-Clause license as part of the BeeWare suite. This constitution defines the non-negotiable engineering principles and governance rules that all contributions — human or AI-assisted — MUST satisfy.

## Core Principles

### I. Cross-Platform Backend Parity

Every public API added to `toga-core` MUST be backed by a concrete implementation plan for the supported production backends (Cocoa, GTK, Qt, Winforms, iOS, Android, Textual, Web). A core API MUST NOT be merged unless it is either (a) implemented on every production backend, or (b) accompanied by a documented, time-boxed `NotImplementedError` surface and a tracking issue per missing backend.

The Dummy backend MUST always implement the full core API surface so that `toga-core` tests can run without a GUI.

Rationale: Toga's value proposition is that a single Python codebase renders natively everywhere. Backend drift silently erodes that contract; making parity a merge precondition prevents the library from accumulating platform-exclusive features disguised as cross-platform ones.

### II. Native Look, Feel, and Behavior

Widgets MUST delegate presentation, input handling, accessibility, and platform conventions to the host operating system's native toolkit. Custom drawing, emulated controls, or cross-platform re-skinning of native widgets are prohibited in production backends unless the host platform offers no native equivalent; any such exception MUST be justified in the PR and recorded in the backend's documentation.

Rationale: "Native" is not a marketing term — it is the user-visible behaviour contract (keyboard shortcuts, focus rings, scroll physics, screen reader semantics, dark-mode response) that distinguishes Toga from web-view wrappers. Violating this principle breaks the product promise made on the project homepage.

### III. Comprehensive Automated Testing (NON-NEGOTIABLE)

All new or modified Toga code MUST ship with automated tests, and merged changes MUST maintain 100% branch coverage for `toga-core` and Travertino as reported by `tox -m test`. Backend behaviour MUST be validated by the testbed app (`briefcase dev --app testbed --test` or equivalent `briefcase run` for mobile) on every backend the change affects.

- Core/Travertino changes: unit tests under the respective `tests/` directory, run via `tox -m test-core` / `tox -m test-trav`.
- Backend changes: probes and scenarios under `testbed/`.
- Bug fixes MUST include a regression test that fails before the fix and passes after.
- Coverage decreases MUST NOT be waived with `# pragma: no cover` except for the cases already whitelisted in the root `pyproject.toml` coverage rules.

Rationale: Toga supports seven production backends across desktop and mobile; without mechanical, enforced coverage the combinatorial space becomes untestable and regressions reach users. 100% coverage is an existing, documented contract of the project and is preserved here as a constitutional rule.

### IV. Public API Stability and Documented Change

Every change visible to Toga users MUST be accompanied by:

1. A change note file in `changes/` named `<issue-or-PR-number>.<kind>.md` where `<kind>` is one of `feature`, `bugfix`, `removal`, `doc`, or `misc`, following the existing towncrier convention.
2. User-facing documentation under `docs/en/` for any new feature, new public API, or behavioural change. Reference material MUST be updated alongside the code — documentation is not a follow-up task.
3. An explicit deprecation path for any removal or incompatible change: at minimum one release carrying a `DeprecationWarning` before the behaviour is removed, and a `removal` change note when the removal lands. Breaking changes without a deprecation period require MAJOR version justification in the PR description.

Rationale: Toga is a public library with downstream applications; silent behavioural drift is indistinguishable from breakage for those users. Change notes and docs are the audit trail that makes semantic versioning honest.

### V. Contributor Accountability

Contributors are responsible for the changes they submit, regardless of how those changes were produced. Specifically:

- PRs MUST follow the documented submission process (branch from `main`, pre-commit checks pass, change note included, CI green).
- Use of autonomous coding tools is permitted but the submitter bears full responsibility for correctness, licensing compatibility, and adherence to this constitution; the BeeWare AI Policy applies in full.
- Reviewers MUST verify the change against the principles above before approving; a PR that fails any principle MUST be rejected or revised, not merged with a waiver.
- All participation is governed by the BeeWare Code of Conduct.

Rationale: Automation and scale make it tempting to treat review as rubber-stamping. Binding the human on both sides of the PR to the same principles keeps quality independent of who (or what) typed the diff.

## Additional Constraints

**Supported runtime platforms**: Toga MUST continue to support the Python versions listed in `core/pyproject.toml` classifiers and the backends enumerated under the repository root (`cocoa/`, `gtk/`, `qt/`, `iOS/`, `android/`, `winforms/`, `textual/`, `web/`). Dropping a supported Python version or backend requires a MINOR-or-greater release and an explicit deprecation notice in `changes/`.

**Toolchain**: The canonical developer toolchain is `tox` for tests, `ruff` for lint and import sorting (configured in root `pyproject.toml`), `pre-commit` for local enforcement, `briefcase` for packaging and testbed execution, and `towncrier` for release-note assembly. Alternative tools are permitted locally but MUST NOT replace these in CI or documented contributor workflows without a constitutional amendment.

**Licensing**: All first-party code MUST remain BSD-3-Clause compatible. Dependencies with incompatible licenses MUST NOT be added to runtime requirements of `toga-core`, Travertino, or any production backend.

**Style**: Code MUST satisfy the Toga code style guide and the automated checks configured in `pre-commit`. Style disagreements are resolved by the style guide, not by individual PR debate.

## Development Workflow

1. **Issue or proposal first**: Non-trivial features start with a GitHub issue or discussion so design can be reviewed before implementation effort is spent. Bug fixes MAY skip this if a reproducer is evident.
2. **Feature branch**: Work is performed on a branch off `main`; direct pushes to `main` are prohibited except by release automation.
3. **Local verification**: Before opening a PR, contributors MUST run `tox -m test` (core + Travertino, 100% coverage) and the testbed for any backend their change affects. Pre-commit hooks MUST pass.
4. **Pull request**: PRs MUST include a change note, updated docs where applicable, and a description that references the issue being closed and the backends exercised.
5. **Review**: At least one maintainer review is required. Reviewers MUST explicitly confirm the five Core Principles are upheld. CI MUST be green before merge.
6. **Merge**: Squash-merge is the default; the squash commit message MUST summarise the user-visible change, not the intermediate work.
7. **Release**: Releases are cut from `main` by project maintainers using `towncrier` to assemble release notes from `changes/`. Version numbers follow the scheme declared in `core/pyproject.toml` and the project release policy; Toga's own release versioning is independent of this constitution's version.

## Governance

This constitution supersedes ad-hoc practice. When a contributing document, code comment, or review conflicts with the constitution, the constitution prevails and the conflicting document MUST be updated.

**Amendment procedure**: Proposed amendments are opened as a PR that edits this file, with a description explaining the motivation, the principle(s) affected, and the version bump being requested. Amendments MUST be reviewed and approved by at least two project maintainers and MUST update the Sync Impact Report at the top of this file.

**Versioning policy**: This constitution uses semantic versioning independent of Toga's release version.

- **MAJOR**: A principle is removed, a principle's meaning is narrowed or reversed, or a governance rule is dropped.
- **MINOR**: A new principle, section, or materially expanded rule is added.
- **PATCH**: Clarifications, wording, typo fixes, or non-semantic refinements.

**Compliance review**: Every PR review MUST include an explicit check against the Core Principles. Maintainers SHOULD perform a constitutional audit at each minor release of Toga, checking that templates, workflows, and CI continue to enforce these principles; any drift MUST be filed as an issue and resolved before the next release.

**Agent guidance**: Autonomous agents (via `AGENTS.md` or equivalent) operating on this repository MUST load and apply this constitution for any task that changes public API, adds or removes backends, modifies test coverage, or touches release tooling.

**Version**: 1.0.0 | **Ratified**: 2026-04-24 | **Last Amended**: 2026-04-24
