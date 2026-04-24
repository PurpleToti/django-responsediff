# Maintenance Plan — django-responsediff

> Generated on 2026-04-23 from the actual state of the repository.
> Updated on 2026-04-24 after 0.9.0 modernization work.
> Repo: https://github.com/yourlabs/django-responsediff

---

## Current State (as of 0.9.0)

| Item | Value |
|---|---|
| Version in pyproject.toml | 0.9.0 |
| Latest Git tag | `v0.7.11` — **v0.8.0 and v0.9.0 still need tagging** |
| License | MIT |
| Python support | 3.10, 3.11, 3.12, 3.13, 3.14 |
| Django support | 4.2 (LTS), 5.2 (LTS), 6.0 |
| CI | GitHub Actions — `.github/workflows/ci.yml` |
| Dependencies | `beautifulsoup4`, `html5lib` |
| tox.ini coverage | `py{310,311,312,313,314}-dj{42,52,60}` |

---

## Phase 1 — Immediate Actions (Getting Back on Track)

### 1.1 — Remove the `six` dependency

- [x] Verify across the entire codebase (`grep -r "import six"`) that no file uses `six`
- [x] Remove `six` from `install_requires` in `setup.py`
- [x] Verify that tests still pass without `six`

### 1.2 — Set up GitHub Actions CI

- [x] Create `.github/workflows/ci.yml` with correct matrix per Django docs:
  - py3.10/3.11 × dj4.2, dj5.2
  - py3.12 × dj4.2, dj5.2, dj6.0
  - py3.13 × dj5.2, dj6.0
  - py3.14 × dj5.2, dj6.0 (experimental)
  - One job per Python version, loops over Django versions internally
- [x] Remove `.travis.yml`
- [x] Verify that the tests run correctly in CI

### 1.3 — Verify Django 3.x / 4.x / 5.x / 6.x Compatibility

- [x] Run the tests locally with Django 6.0 and Python 3.14
- [x] Fix `settings.py`: added `DEFAULT_AUTO_FIELD`, removed deprecated `USE_L10N`
- [x] Verified `response['Location']` works correctly across all versions
- [x] Fixed test fixtures to be Django-version-independent (replaced admin login page with a controlled view)

### 1.4 — Resolve the Version Inconsistency

- [x] Correct `CHANGES.txt` (added missing 0.8.0 and 0.9.0 entries)
- [ ] Create git tags `v0.8.0` and `v0.9.0`
- [ ] Check on PyPI whether version `0.8.0` is published, publish `0.9.0`

---

## Phase 2 — tox.ini Modernization

- [x] Replace `whitelist_externals` with `allowlist_externals`
- [x] Update `envlist`: `py{310,311,312,313,314}-dj{42,52,60}`
- [x] Update Django `deps`: `dj42: Django>=4.2,<5.0`, `dj52: Django>=5.2,<6.0`, `dj60: Django>=6.0,<7.0`
- [x] Change `basepython = python2.7` → `python3.12` in `[testenv:qa]`
- [x] Replace `flake8` with `ruff` in `[testenv:qa]`
- [x] Remove `mock` and `six` from deps (stdlib `unittest.mock` used instead)

---

## Phase 3 — Current Python and Django Compatibility

### Add Python 3.13, 3.14 and Django 5.2 LTS / 6.0

- [x] Add `py313`, `py314` to `tox.ini` and the GitHub Actions CI
- [x] Add `django52`, `django60` to the test matrix
- [x] Verified that `beautifulsoup4` and `html5lib` are compatible with Python 3.14

### Drop EOL Versions

- [x] Remove all support for Python < 3.10 from the configuration
- [x] Clearly document supported versions in `README.rst`

---

## Phase 4 — Packaging Modernization

### Update `README.rst`

- [x] Rewrite the "Requirements" section: Python 3.10-3.14, Django 4.2-6.0
- [x] Replace Travis CI badge with GitHub Actions badge
- [x] Document `assertWebsiteSame`

### Migrate to `pyproject.toml`

- [x] Migrate to `pyproject.toml` (build-backend `setuptools>=61`)
- [x] Remove `setup.py`
- [x] Update classifiers: drop Python 2 and Django 1.x, add current versions
- [x] Add `ruff` configuration to `pyproject.toml`

### PyPI Publishing and Release Management

- [ ] Create a GitHub Action for automatic PyPI publishing on tag push
- [ ] Tag `v0.8.0` and `v0.9.0`
- [ ] Publish `v0.9.0` to PyPI

---

## Phase 5 — Quality and Tests

### Modernize Existing Tests

- [x] `test_assertNoDiffSelector_non_ascii` now self-cleans its fixture (no longer relies on tox pre-run `rm -rf`)
- [x] Removed orphaned `test_response.py` (belonged to another project)
- [x] Removed brittle hardcoded 404 diff assertion from `test_story`
- [x] Fixed `import mock` → `from unittest import mock` (stdlib)
- [x] `.gitignore` updated: transient test fixtures excluded, stable ones committed

### Evaluate Replacing `html5lib`

- [ ] Check whether `html5lib` is used directly or only as a BeautifulSoup backend
- [ ] Evaluate replacing it with `lxml` as the BS4 backend (faster, well maintained)
- [ ] If replaced, run regression tests against existing fixtures

---

## Summary by Priority

### Done ✅
- **[CI]** GitHub Actions CI with correct Django/Python matrix
- **[MOD]** Removed the `six` dependency
- **[MOD]** Migrated `setup.py` → `pyproject.toml` (v0.9.0)
- **[COMPAT]** Verified and confirmed Django 4.2 / 5.2 / 6.0 compatibility
- **[QA]** Modernized `tox.ini`: `allowlist_externals`, updated envlist and deps
- **[QA]** Replaced `flake8` with `ruff`
- **[COMPAT]** Added Python 3.10–3.14, Django 5.2 LTS and 6.0
- **[COMPAT]** Dropped Python 3.7, Django 2.1 (all EOL)
- **[DOC]** Rewrote README with current versions, GitHub Actions badge, `assertWebsiteSame`
- **[QA]** Fixed test fixture stability across Django versions

### Still pending
- [ ] **[REL]** Tag `v0.8.0` and `v0.9.0`, publish to PyPI
- [ ] **[MOD]** GitHub Action for automatic PyPI release on tag push
- [ ] **[QA]** Evaluate replacing `html5lib` with `lxml` as the BeautifulSoup backend
