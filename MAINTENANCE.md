# Maintenance Plan — django-responsediff

> Generated on 2026-04-23 from the actual state of the repository.
> Repo: https://github.com/yourlabs/django-responsediff

---

## Current State

| Item | Value |
|---|---|
| Version in setup.py | 0.8.0 |
| Latest Git tag | `v0.7.11` (inconsistency with setup.py — 0.8.0 was never tagged) |
| Latest commit | "Strip any pound from urls" |
| License | MIT |
| Python support (declared in README) | 2.7 and 3.4 — **severely outdated** |
| Django support (declared in README) | 1.7 to 1.10 — **severely outdated** |
| CI | Travis CI only (`.travis.yml`) — **Travis CI is dead for open source** |
| Dependencies | `beautifulsoup4`, `html5lib`, `six` |
| tox.ini coverage | `py{37,py}-dj{21}` — Django 2.1 and Python 3.7 only |

**Critical situation:** This repository is effectively abandoned. CI is completely broken (Travis CI), the README describes versions from 2016, and no tests have been run in CI for several years. Compatibility with Django 3.x, 4.x, and 5.x is unknown.

**Positive note:** The source code (`response.py`) is short (~212 lines), clean, and has no exotic dependencies. The logic is simple and likely still functional.

---

## Phase 1 — Immediate Actions (Getting Back on Track)

### 1.1 — Remove the `six` dependency

`six` is a Python 2/3 compatibility library, useless since Python 2 reached EOL in January 2020. It is listed in `setup.py` but **is not imported anywhere in the source code** (`response.py`, `test.py`, `exceptions.py` do not use it). It is a ghost dependency that bloats installations for no reason.

**Actions:**
- [ ] Verify across the entire codebase (`grep -r "import six"`) that no file uses `six`
- [ ] Remove `six` from `install_requires` in `setup.py`
- [ ] Verify that tests still pass without `six`

### 1.2 — Set up GitHub Actions CI

Travis CI no longer works for open source projects without a paid subscription. Migration to GitHub Actions is required.

**Actions:**
- [ ] Create `.github/workflows/django.yml` with a minimal starting matrix:
  - Python 3.10, 3.11, 3.12, 3.13, 3.14
  - Django 4.2, 5.2, 6.0
  - SQLite only (responsediff does not test the database directly)
- [ ] Remove `.travis.yml` (or keep it commented during transition)
- [ ] Verify that the tests run correctly in this new environment

### 1.3 — Verify Django 3.x / 4.x / 5.x Compatibility

Compatibility with recent Django versions is unknown. The code uses `response['Content-Type']` and `response.content`, which are stable APIs, but Django changes may have broken edge case behavior.

**Actions:**
- [ ] Run the tests locally with Django 4.2 and Python 3.11
- [ ] Identify and fix any `DeprecationWarning` or errors
- [ ] In particular: verify `response['Location']` (redirect header) on Django 5.x

### 1.4 — Resolve the Version Inconsistency

`setup.py` declares version `0.8.0` but the latest Git tag is `v0.7.11`. Version `0.8.0` was never properly tagged or released.

**Actions:**
- [ ] Create tag `v0.8.0` pointing to the "Release 0.8.0" commit
- [ ] Check on PyPI whether version `0.8.0` is published, and publish it if not
- [ ] Correct `CHANGES.txt` if necessary

---

## Phase 2 — tox.ini Modernization

The current `tox.ini` is in a critical state:

| Problem | Detail |
|---|---|
| `envlist = py{37,py}-dj{21}` | Python 3.7 (EOL June 2023), Django 2.1 (EOL Dec 2019) |
| `whitelist_externals` | Deprecated since tox 3.18, replaced by `allowlist_externals` |
| `basepython = python2.7` in `[testenv:qa]` | Python 2 has been EOL since 2020 |

**Actions:**
- [ ] Replace `whitelist_externals` with `allowlist_externals`
- [ ] Update `envlist`: `py{310,311,312,313,314}-dj{42,52,60}`
- [ ] Update Django `deps`: `dj42: Django>=4.2,<5.0`, `dj52: Django>=5.2,<6.0`, `dj60: Django>=6.0,<7.0`
- [ ] Change `basepython = python2.7` → `python3.12` in `[testenv:qa]`
- [ ] Update `[gh-actions]` to align with the new versions

---

## Phase 3 — Current Python and Django Compatibility

### Add Python 3.13, 3.14 and Django 5.2 LTS / 6.0

**Actions:**
- [ ] Add `py313`, `py314` to `tox.ini` and the GitHub Actions CI
- [ ] Add `django52`, `django60` to the test matrix
- [ ] Verify that `beautifulsoup4` and `html5lib` are compatible with Python 3.13 and 3.14

### Drop EOL Versions

- Python 3.7: EOL June 2023
- Django 2.1: EOL December 2019
- Django 3.x: EOL April 2024

**Actions:**
- [ ] Remove all support for Python < 3.10 from the configuration
- [ ] Clearly document supported versions in `README.rst`

---

## Phase 4 — Packaging Modernization

### Update `README.rst`

The README describes Django 1.7-1.10 and Python 2.7/3.4 — it dates from ~2016.

**Actions:**
- [ ] Rewrite the "Requirements" section: Python 3.10-3.14, Django 4.2-6.0
- [ ] Replace Travis CI badges with GitHub Actions badges
- [ ] Update the Codecov badge with the current URL
- [ ] Document `assertWebsiteSame` (absent from the README)

### Migrate to `pyproject.toml`

`setup.py` predates PEP 517/518.

**Actions:**
- [ ] Migrate to `pyproject.toml` (build-backend `hatchling` or `setuptools>=61`)
- [ ] Remove `setup.py`
- [ ] Update classifiers: drop Python 2 and Django 1.x, add current versions

### PyPI Publishing and Release Management

**Actions:**
- [ ] Create a GitHub Action for automatic PyPI publishing on tag push
- [ ] Properly tag all untagged versions (`v0.8.0`)
- [ ] Publish `v0.9.0` after the compatibility updates

---

## Phase 5 — Quality and Tests

### Modernize Existing Tests

`tox.ini` deletes fixtures via `rm -rf` before each run — a fragile approach.

**Actions:**
- [ ] Verify whether the fixture cleanup at the start of tests is still necessary
- [ ] If possible, handle cleanup at the test level (`setUp`/`tearDown`)
- [ ] Add a test covering the `FIXTURE_REWRITE=1` case

### Evaluate Replacing `html5lib`

`html5lib` is slow and poorly maintained. `lxml` or BeautifulSoup's built-in parser are faster alternatives.

**Actions:**
- [ ] Check whether `html5lib` is used directly or only as a BeautifulSoup backend
- [ ] Evaluate replacing it with `lxml` as the BS4 backend (faster, well maintained)
- [ ] If replaced, run regression tests against existing fixtures

---

## Summary by Priority

### Critical (CI restoration and consistency)
- [ ] **[CI]** Create `.github/workflows/django.yml` — Travis CI is dead, there is no CI at all
- [ ] **[BUG]** Tag `v0.8.0` and verify PyPI publication (version/tag inconsistency)
- [ ] **[MOD]** Remove the `six` dependency (ghost dependency, useless since Python 2 EOL)
- [ ] **[COMPAT]** Verify Django 4.2 and 5.x compatibility by running the tests

### High priority (tox modernization)
- [ ] **[QA]** Replace `whitelist_externals` → `allowlist_externals` in `tox.ini`
- [ ] **[COMPAT]** Update `envlist`: Python 3.10-3.14, Django 4.2-6.0
- [ ] **[QA]** Change `basepython = python2.7` → `python3.12` in `[testenv:qa]`

### Normal priority (compatibility)
- [ ] **[COMPAT]** Add Python 3.13, 3.14 and Django 5.2 LTS, 6.0
- [ ] **[COMPAT]** Drop Python 3.7, Django 2.1 and 3.x (all EOL)
- [ ] **[DOC]** Rewrite README with current supported versions and GitHub Actions badges

### Normal priority (modernization)
- [ ] **[MOD]** Migrate from `setup.py` to `pyproject.toml`
- [ ] **[MOD]** GitHub Action for automatic PyPI release on tag push
- [ ] **[REL]** Publish `v0.9.0` after compatibility updates

### Low priority
- [ ] **[QA]** Evaluate replacing `html5lib` with `lxml` as the BeautifulSoup backend
- [ ] **[QA]** Evaluate migrating `flake8` → `ruff`
- [ ] **[DOC]** Document `assertWebsiteSame` in the README (currently absent)
