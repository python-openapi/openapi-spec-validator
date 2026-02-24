# AGENTS.md
Guidance for coding agents working in `openapi-spec-validator`.

## Project Snapshot
- Language: Python (3.10-3.14)
- Tooling: Poetry, pytest, mypy, black, isort, flake8, deptry, pre-commit, tox
- Main package: `openapi_spec_validator/`
- Tests: `tests/integration/`, `tests/bench/`
- Docs: Sphinx in `docs/`

## Setup
- Keep venv in-project: `poetry config virtualenvs.in-project true`
- Install dev deps: `poetry install --with dev`
- Install docs deps: `poetry install --with docs`

## Build Commands
- Build artifacts: `poetry build`
- Legacy build path: `make dist-build`
- Clean build/test artifacts: `make cleanup`

## Test Commands
- Full tests: `poetry run pytest`
- Multi-Python matrix locally: `tox`
- One file: `poetry run pytest tests/integration/test_main.py`
- One test function: `poetry run pytest tests/integration/test_main.py::test_version`
- One parametrized case:
  `poetry run pytest 'tests/integration/validation/test_validators.py::TestLocalOpenAPIv30Validator::test_valid[petstore.yaml]'`
- By keyword: `poetry run pytest -k "schema_v31"`
- Exclude network tests: `poetry run pytest -m "not network"`
- Run only network tests: `poetry run pytest -m network`
- Fast focused test without default addopts (no coverage/junit):
  `poetry run pytest -o addopts='' tests/integration/test_main.py::test_version`

## Lint, Format, Type, Dependencies
- Format: `poetry run black . && poetry run isort .`
- Format check only: `poetry run black --check . && poetry run isort --check-only .`
- Lint: `poetry run flake8`
- Types: `poetry run mypy`
- Dependency check: `poetry run deptry .`
- Pre-commit setup: `pre-commit install`
- Run all hooks: `pre-commit run --all-files`

## Docs
- CI-equivalent docs build:
  `poetry run python -m sphinx -T -b html -d docs/_build/doctrees -D language=en docs docs/_build/html -n -W`

## Style Rules (from repo config + code)

### Formatting
- Black is authoritative formatter.
- Line length is 79 (`tool.black.line-length = 79`, flake8 79).
- isort uses `profile = black` and `force_single_line = true`.
- Keep one imported symbol per line for `from x import y` style blocks.

### Imports
- Use absolute imports from `openapi_spec_validator...`.
- Order import groups: stdlib, third-party, first-party.
- Avoid wildcard imports.
- Keep imports explicit and deterministic under isort.

### Typing
- Mypy is strict (`[tool.mypy] strict = true`).
- Add annotations to all new/modified functions and methods.
- Prefer built-in generics (`list[str]`, `dict[str, int]`) and `X | None`.
- Avoid broad `Any`; if unavoidable, keep scope minimal.
- Existing ignores are for external libs only; do not add broad ignores casually.

### Naming
- Modules/files: `snake_case`.
- Variables/functions: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Test functions: `test_*` and behavior-focused names.

### Error Handling
- Raise specific exceptions in library code.
- Preserve public exception behavior unless change is intentional and tested.
- CLI in `openapi_spec_validator/__main__.py` currently uses:
  - exit code 1 for read/validation failures
  - exit code 2 for unexpected runtime failures
- Keep deprecation warnings consistent with current message patterns.
- Do not discard useful validation context when propagating errors.

### Tests and Markers
- Use pytest assertions directly (`assert ...`).
- Reuse helpers in `tests/integration/conftest.py`.
- Mark network-dependent tests with `@pytest.mark.network`.
- Prefer integration tests near affected behavior (`validation`, `shortcuts`, `versions`, CLI).
- If behavior changes, add/adjust tests in the same PR.

## CI Expectations
- Main CI test workflow runs on Python 3.10-3.14 and ubuntu/windows.
- Core checks are:
  1. `poetry run pytest`
  2. `poetry run mypy`
  3. `poetry run deptry .`
- Pre-commit hooks include: pyupgrade (`--py310-plus`), black, isort, flake8.
- Docs CI installs `--with docs` and runs Sphinx with `-n -W` (warnings are failures).

## Compatibility Notes
- Project keeps deprecated compatibility paths (e.g., old flags and shortcuts).
- Avoid removing aliases or changing warning behavior without explicit instruction.
- Keep CLI/user-facing strings stable unless tests are updated accordingly.

## Cursor/Copilot Instructions Check
- `.cursor/rules/`: not present
- `.cursorrules`: not present
- `.github/copilot-instructions.md`: not present
- If these files appear later, treat them as higher-priority agent instructions and update this file.

## Agent Working Agreement
- Keep diffs minimal and scoped.
- Do not modify unrelated files.
- Prefer targeted tests first, then full suite when needed.
- Run formatter/lint/type checks for code changes before finishing.
- Maintain backward compatibility unless task explicitly requests breaking change.

## Handy Paths
- Package entrypoint: `openapi_spec_validator/__main__.py`
- API shortcuts: `openapi_spec_validator/shortcuts.py`
- Validators: `openapi_spec_validator/validation/validators.py`
- Reader utilities: `openapi_spec_validator/readers.py`
- Integration tests: `tests/integration/`
- Pyproject config: `pyproject.toml`
- Tox config: `tox.ini`
- Pre-commit config: `.pre-commit-config.yaml`

## Quick Local Validation Recipe
Run this sequence before handoff:
1. `poetry run black . && poetry run isort .`
2. `poetry run flake8`
3. `poetry run mypy`
4. `poetry run pytest -m "not network"`
5. Add targeted network test runs only if your change touches URL/network behavior.

## Practical Execution Notes
- Pytest defaults from `pyproject.toml` include coverage and junit outputs.
- For quick iterations, prefer `-o addopts=''` with a specific node id.
- Keep command output readable; avoid noisy full-suite runs unless needed.
- For CLI behavior changes, prioritize tests in `tests/integration/test_main.py`.
- For validator behavior changes, prioritize `tests/integration/validation/`.
- For version detection changes, prioritize `tests/integration/test_versions.py`.

## Commit/PR Hygiene for Agents
- Keep changes scoped to the requested task.
- Do not bundle formatting-only churn with behavior changes unless requested.
- Mention any intentionally preserved deprecated behavior in PR notes.
- If you change user-visible messages, update tests in the same change.
