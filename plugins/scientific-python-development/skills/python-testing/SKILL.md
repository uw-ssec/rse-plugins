---
name: python-testing
description: Use when writing or organizing tests for scientific Python code, or when the user mentions pytest, test fixtures, parametrization, numerical assertions, or property-based testing. Write and organize tests for scientific Python packages using pytest. Covers fixtures, parametrization, numerical testing with NumPy utilities, property-based testing with Hypothesis, and CI integration.
metadata:
  assets:
    - assets/conftest-example.py
    - assets/github-actions-tests.yml
    - assets/pyproject-pytest.toml
  references:
    - references/common-pitfalls.md
    - references/scientific-patterns.md
    - references/test-patterns.md
---

# Scientific Python Testing with pytest

## Quick Reference

### Choose the right assertion

```python
# Scalar floating-point → pytest.approx (default rel=1e-6)
from pytest import approx
assert result == approx(0.333, rel=1e-6)
assert result == approx(0.0, abs=1e-10)   # near-zero: use abs tolerance

# NumPy array, element-wise → approx works; for complex tolerances use numpy.testing
assert np.array([0.1, 0.2]) == approx(np.array([0.1, 0.2]))
np.testing.assert_allclose(result, expected, rtol=1e-7, atol=1e-10)

# Exact integer arrays
np.testing.assert_array_equal(result, expected)

# Exceptions
with pytest.raises(ValueError, match="must be positive"):
    compute_sqrt(-1)

# Warnings
with pytest.warns(DeprecationWarning):
    old_function()

# Multiple inputs → parametrize
@pytest.mark.parametrize("x,expected", [(0, 0), (2, 4), (-2, 4)])
def test_square(x, expected):
    assert x**2 == expected

# Reusable setup → fixture
@pytest.fixture
def sample_data():
    return np.array([1.0, 2.0, 3.0, 4.0, 5.0])

def test_mean(sample_data):
    assert np.mean(sample_data) == approx(3.0)

# Property-based (Hypothesis)
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays

@given(arrays(np.float64, shape=st.integers(1, 50),
              elements=st.floats(-100, 100, allow_nan=False)))
def test_mean_bounded(arr):
    assert np.min(arr) <= np.mean(arr) <= np.max(arr)
```

### pytest configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = ["-ra", "--showlocals", "--strict-markers", "--strict-config"]
testpaths = ["tests"]
markers = [
    "slow: mark test as slow",
    "integration: mark as integration test",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
```

See `assets/pyproject-pytest.toml` for the complete annotated configuration and `assets/conftest-example.py` for shared fixtures.

### Project layout

```
my-package/
├── src/my_package/
├── tests/
│   ├── conftest.py        ← shared fixtures
│   ├── test_analysis.py
│   └── test_utils.py
└── pyproject.toml
```

No `__init__.py` in `tests/`. Install with `pip install -e .` so tests run against the installed package.

---

## Patterns and Reference

| Reference | Contents |
|-----------|----------|
| `references/test-patterns.md` | Focused tests (Arrange-Act-Assert), exceptions/warnings, floating-point comparisons, fixtures with scope and teardown, parametrization with custom IDs, markers (slow/skip/xfail), directory-based test suites, mocking/monkeypatching |
| `references/scientific-patterns.md` | Numerical stability and convergence tests, dtype parametrization, stochastic code with fixed seeds, data pipeline testing, Hypothesis property-based testing |
| `references/common-pitfalls.md` | Testing implementation vs. behaviour, non-deterministic tests, exact float comparisons, testing too much in one test |

Non-obvious gotchas:
- **`approx` vs `assert_allclose`**: `pytest.approx` is cleaner for most cases; use `numpy.testing.assert_allclose` when you need different `rtol`/`atol` per element or need better error messages for large arrays.
- **`abs` tolerance near zero**: `approx(0.0)` with default relative tolerance always passes — always pass `abs=` when the expected value is or could be zero.
- **`--strict-markers`**: add it from day one; it turns typo'd marker names into errors rather than silent no-ops.
- **Fixture scope**: `scope="session"` fixtures are shared across the whole run — any mutation bleeds into other tests. Use `scope="module"` for read-only shared data; keep mutable fixtures at `scope="function"`.
- **Random seeds**: prefer `np.random.default_rng(42)` over `np.random.seed(42)`; the latter sets global state and can interact with other tests.
- **`tmp_path` built-in**: pytest provides `tmp_path` (a `pathlib.Path` to a per-test temp dir) for free — no need to write your own temp-file fixture.

---

## Commands

```bash
# Run
pytest                              # all tests
pytest tests/test_analysis.py      # one file
pytest tests/test_analysis.py::test_mean  # one test
pytest -k "mean or median"          # pattern match
pytest -m "not slow"                # skip slow tests

# Debug
pytest -x                           # stop at first failure
pytest --lf                         # rerun last failures only
pytest --pdb                        # drop into debugger on failure
pytest --collect-only               # dry run (see what would run)

# Coverage
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-fail-under=80
```

---

## Workflow: Write → Verify → Ship

```
1. Write the test
   └─ Run it: pytest tests/test_foo.py::test_new -v
      └─ It should FAIL (if it passes on unwritten code, the test is wrong)

2. Write the implementation

3. Run the test again
   └─ It should now PASS

4. Run the full suite
   └─ pytest -x   (stop on first regression)

5. Check coverage
   └─ pytest --cov=src --cov-report=term-missing
      └─ Are the new lines covered?

6. Commit
   └─ All tests green, coverage threshold met
```

**Checkpoint: always verify a new test fails before the implementation exists.**  
A test that passes on broken code gives false confidence and will never catch regressions.

---

## CI Integration

See `assets/github-actions-tests.yml` for a ready-to-use GitHub Actions workflow (matrix across Python versions, coverage upload).

Minimal workflow step:

```yaml
- name: Run tests
  run: pytest --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v4
```
