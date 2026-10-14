# Test, coverage, and CI standardization — design

- Date: 2026-10-14
- Issues: biocommons/python-package#106, biocommons/.github#10
- Status: approved design; pending implementation plan

## Context

`python-package` is the template for biocommons Python packages. Its test, coverage, and CI setup had drifted:

- `make test` and `make test-coverage` were effectively identical because `--cov=src` was in pytest `addopts`.
- Coverage was always on, which can stop IDE debugger breakpoints from firing, and nothing enforced a coverage threshold except Codecov's fixed `target: 90%`.
- `tox` did not test multiple Python versions: `uv run` inside each tox env ignores `VIRTUAL_ENV` and uses the project `.venv` (verified: the `py311` env ran Python 3.15).
- `.github/workflows/github-coverage.yml` failed on every push because nothing generated `coverage.xml`.
- The shared workflow (`biocommons/.github/.github/workflows/python-ci-cd.yml`) called some tools directly instead of through make, and all callers pinned it at `@main`.

## Goals

1. Simplicity and least surprise.
2. make is the single interface; local, tox, and GitHub Actions invoke the same targets.
3. IDE testing works with minimal configuration; tox works; CI fails when coverage drops.
4. A target and coverage contract that other-language templates (Rust, Go) can adopt.

## Decisions

| # | Decision | Rejected alternatives |
|---|----------|-----------------------|
| 1 | Coverage gate is Codecov `target: auto` in CI only; nothing fails on coverage locally. | Local `fail_under` floor plus Codecov; Codecov fixed floor as a second status. |
| 2 | Codecov is the only coverage service; delete `github-coverage.yml`. | Keep both; GitHub coverage only. |
| 3 | Two targets: `test` (no coverage) and `test-coverage` (coverage + Cobertura XML). | Single `test` target always with coverage. |
| 4 | tox is a local multi-version runner using the standard tox-uv lock runner; CI does not use tox; `cqa` is not run in tox. | tox → make via `UV_PROJECT_ENVIRONMENT`. |
| 5 | Version the shared workflow; downstream repos pin the old behavior before the new behavior lands. | Change `@main` with coordinated PRs; backward-compatible conditional in shared CI. |
| 6 | Only one matrix leg (`coverage-python-version`, currently 3.15) uploads coverage. | Upload all legs with `after_n_builds`. |
| 7 | Ship no IDE config; README documents the one-time VS Code setup. | Commit `.vscode/settings.json`. |
| 8 | Minimal `addopts`: only flags that affect correctness. Use first-class config options where pytest provides them. | Default marker filters; leaving current flags. |
| 9 | Shared-workflow tags: fixed semver without `v` (`1.0.0`) plus a moving major tag (`1`). | Moving major tags only; fixed semver only. |

## Design

### 1. make contract (language-neutral)

| Target | Meaning (any language) | Python implementation | Called by CI |
|---|---|---|---|
| `devready` | Set up the dev environment | unchanged | no |
| `cqa` | Lint, format, and static checks | unchanged | yes |
| `test` | Tests, no coverage | `uv run pytest` | no |
| `test-coverage` | Tests with coverage; terminal report and `coverage.xml` (Cobertura) at repo root | `uv run pytest --cov --cov-report=term-missing --cov-report=xml` | yes, every matrix leg |
| `docs-test` | Strict docs build | `uv run mkdocs build -s` | yes |
| `docs-deploy` | Deploy docs (new) | `uv run mkdocs gh-deploy --force` | yes, on tags |
| `build` | Build artifacts | unchanged | via `publish` |
| `publish` | Build and release | unchanged (depends on `build`) | yes, on tags |
| `tox` | Python only: tests on each version, locally | `uv run tox` | no |

- `--cov` without an argument uses `[tool.coverage.run] source = ["src"]`, so coverage scope is defined in one place.
- The fixed `coverage.xml` name and Cobertura format keep the shared CI language-neutral. Rust: `cargo llvm-cov --cobertura`. Go: needs a converter (e.g., `gocover-cobertura`); that dependency belongs to a future Go template.

### 2. Python configuration

Config keys and sections are alphabetically sorted where order is not semantic.

`pyproject.toml`, `[tool.pytest.ini_options]` (`doctest_optionflags` unchanged):

```toml
addopts = "--doctest-modules"
markers = [
  "extra: optional tests; deselect with -m 'not extra'",
  "network: tests that require network connectivity",
  "slow: slow tests that should be run infrequently"
]
strict_markers = true
testpaths = ["src", "tests"]
```

- `--doctest-modules` has no config-option equivalent in pytest 9.1.1, so it stays in `addopts`.
- `strict_markers` is preferred over `strict`, whose set of checks may grow with pytest upgrades.
- Markers do not deselect tests by themselves. The template declares `extra` but does not filter it; repos that want extra tests excluded by default add `-m 'not extra'` to their own `addopts`. Note that `-m` is last-wins: a CLI `-m` replaces an `addopts` `-m`.
- No `fail_under` (decision 1). `[tool.coverage.*]` is unchanged.

`tox.ini` (replaced):

```ini
[testenv]
commands = pytest {posargs}
dependency_groups = dev
runner = uv-venv-lock-runner
setenv =
    PYTHONHASHSEED = 0

[tox]
envlist = py311, py312, py313, py314, py315
```

- Removed: `skipsdist`, `[gh-actions]`, `passenv = PYTHON_VERSION`, and the `make devready` / `make cqa` commands.
- To verify during implementation: tox-uv provisions missing Python versions by default; `dependency_groups = dev` is required by the lock runner.
- Acceptance check: each tox env reports its own Python version.

### 3. CI

`biocommons/.github` (biocommons/.github#10), in order:

1. Tag current `main` as `1.0.0` and `1`.
2. Pin downstream callers from `@main` to `@1`: hgvs, bioutils, biocommons.seqrepo, seqrepo-rest-service. These must merge before step 3 lands on `main`.
3. Change `python-ci-cd.yml`:
   - `test`: `make test` → `make test-coverage`; Codecov upload on the `coverage-python-version` leg only, with explicit `files: coverage.xml`.
   - `check-docs`: `uv run mkdocs build -s` → `make docs-test`.
   - `publish-package`: `uv build` + `uv publish` → `make publish`, keeping `UV_PUBLISH_TOKEN`.
   - `deploy-docs`: `uv run mkdocs gh-deploy --force` → `make docs-deploy`.
4. Merge, then tag `2.0.0` and `2`. Later fixes get a patch tag and re-point the major tag.

`python-package` (biocommons/python-package#106):

1. Delete `.github/workflows/github-coverage.yml`.
2. Change `python-ci-cd.yml` to `@2` once `2.0.0` exists.
3. `codecov.yaml`: project `default.target: 90%` → `auto`, keeping `threshold: 0.5%`.
4. README: VS Code setup (Testing → Configure Python Tests → pytest); note that `codecov/project` must be a required status check in branch protection, or the gate does nothing.

## Testing and acceptance

- `make test` runs without coverage instrumentation and produces no coverage output.
- `make test-coverage` prints the `term-missing` table and writes `coverage.xml`.
- `make tox` runs each env on its own Python version.
- VS Code test explorer discovers and runs tests, and breakpoints hit, with no workspace settings beyond enabling pytest.
- CI on `@2`: all matrix legs pass `make test-coverage`; Codecov receives one upload and posts a `codecov/project` status.
- Downstream repos on `@1` are unaffected by the `@2` changes.

## Out of scope

- The `make cqa` failure on `main`.
- The outdated `setup-python-env` action (uv 0.7.14, setup-python@v5, default Python 3.13).
- pytest-optional-tests fixes (tracked in reece/pytest-optional-tests#8).
