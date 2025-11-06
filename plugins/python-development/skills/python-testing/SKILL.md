---
name: scientific-python-testing
description: Write robust, maintainable tests for scientific Python packages using pytest best practices following Scientific Python community guidelines
---

# Scientific Python Testing with pytest

A comprehensive guide to writing effective tests for scientific Python packages using pytest, following the [Scientific Python Community guidelines](https://learn.scientific-python.org/development/guides/pytest/) and [testing tutorial](https://learn.scientific-python.org/development/tutorials/test/). This skill focuses on modern testing patterns, fixtures, parametrization, and best practices specific to scientific computing.

## Quick Reference Card

**Common Testing Tasks - Quick Decisions:**

```python
# 1. Basic test → Use simple assert
def test_function():
    assert result == expected

# 2. Floating-point comparison → Use approx
from pytest import approx
assert result == approx(0.333, rel=1e-6)

# 3. Testing exceptions → Use pytest.raises
with pytest.raises(ValueError, match="must be positive"):
    function(-1)

# 4. Multiple inputs → Use parametrize
@pytest.mark.parametrize("input,expected", [(1,1), (2,4), (3,9)])
def test_square(input, expected):
    assert input**2 == expected

# 5. Reusable setup → Use fixture
@pytest.fixture
def sample_data():
    return np.array([1, 2, 3, 4, 5])

# 6. NumPy arrays → Use approx or numpy.testing
assert np.mean(data) == approx(3.0)
```

**Decision Tree:**
- Need multiple test cases with same logic? → **Parametrize**
- Need reusable test data/setup? → **Fixture**
- Testing floating-point results? → **pytest.approx**
- Testing exceptions/warnings? → **pytest.raises / pytest.warns**
- Complex numerical arrays? → **numpy.testing.assert_allclose**
- Organizing by speed? → **Markers and separate directories**

## When to Use This Skill

- Writing tests for scientific Python packages and libraries
- Testing numerical algorithms and scientific computations
- Setting up test infrastructure for research software
- Implementing continuous integration for scientific code
- Testing data analysis pipelines and workflows
- Validating scientific simulations and models
- Ensuring reproducibility and correctness of research code
- Testing code that uses NumPy, SciPy, Pandas, and other scientific libraries

## Core Concepts

### 1. Why pytest for Scientific Python

pytest is the de facto standard for testing Python packages because it:

- **Simple syntax**: Just use Python's `assert` statement
- **Detailed reporting**: Clear, informative failure messages
- **Powerful features**: Fixtures, parametrization, marks, plugins
- **Scientific ecosystem**: Native support for NumPy arrays, approximate comparisons
- **Community standard**: Used by NumPy, SciPy, Pandas, scikit-learn, and more

### 2. Test Structure and Organization

**Standard test directory layout:**

```text
my-package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── analysis.py
│       └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_analysis.py
│   └── test_utils.py
└── pyproject.toml
```

**Key principles:**

- Tests directory separate from source code (alongside `src/`)
- Test files named `test_*.py` (pytest discovery)
- Test functions named `test_*` (pytest discovery)
- No `__init__.py` in tests directory (avoid importability issues)
- Test against installed package, not local source

### 3. pytest Configuration

Configure pytest in `pyproject.toml` (recommended for modern packages):

```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",              # Show summary of all test outcomes
    "--showlocals",     # Show local variables in tracebacks
    "--strict-markers", # Error on undefined markers
    "--strict-config",  # Error on config issues
]
xfail_strict = true     # xfail tests must fail
filterwarnings = [
    "error",            # Treat warnings as errors
]
log_cli_level = "info"  # Log level for test output
testpaths = [
    "tests",            # Limit pytest to tests directory
]
```

## Testing Principles

Following the [Scientific Python testing recommendations](https://learn.scientific-python.org/development/principles/testing/), effective testing provides multiple benefits and should follow key principles:

### Advantages of Testing

- **Trustworthy code**: Well-tested code behaves as expected and can be relied upon
- **Living documentation**: Tests communicate intent and expected behavior, validated with each run
- **Preventing failure**: Tests protect against implementation errors and unexpected dependency changes
- **Confidence when making changes**: Thorough test suites enable adding features, fixing bugs, and refactoring with confidence

### Fundamental Principles

**1. Any test case is better than none**

When in doubt, write the test that makes sense at the time:
- Test critical behaviors, features, and logic
- Write clear, expressive, well-documented tests
- Tests are documentation of developer intentions
- Good tests make it clear what they are testing and how

Don't get bogged down in taxonomy when learning—focus on writing tests that work.

**2. As long as that test is correct**

It's surprisingly easy to write tests that pass when they should fail:
- **Check that your test fails when it should**: Deliberately break the code and verify the test fails
- **Keep it simple**: Excessive mocks and fixtures make it difficult to know what's being tested
- **Test one thing at a time**: A single test should test a single behavior

**3. Start with Public Interface Tests**

Begin by testing from the perspective of a user:
- Test code as users will interact with it
- Keep tests simple and readable for documentation purposes
- Focus on supported use cases
- Avoid testing private attributes
- Minimize use of mocks/patches

**4. Organize Tests into Suites**

Divide tests by type and execution time for efficiency:
- **Unit tests**: Fast, isolated tests of individual components
- **Integration tests**: Tests of component interactions and dependencies
- **End-to-end tests**: Complete workflow testing

Benefits:
- Run relevant tests quickly and frequently
- "Fail fast" by running fast suites first
- Easier to read and reason about
- Avoid false positives from expected external failures

### Outside-In Testing Approach

The recommended approach is **outside-in**, starting from the user's perspective:

1. **Public Interface Tests**: Test from user perspective, focusing on behavior and features
2. **Integration Tests**: Test that components work together and with dependencies
3. **Unit Tests**: Test individual units in isolation, optimized for speed

This approach ensures you're building the right thing before optimizing implementation details.

## Quick Start

### Minimal Test Example

```python
# tests/test_basic.py

def test_simple_math():
    """Test basic arithmetic."""
    assert 4 == 2**2

def test_string_operations():
    """Test string methods."""
    result = "hello world".upper()
    assert result == "HELLO WORLD"
    assert "HELLO" in result
```

### Scientific Test Example

```python
# tests/test_scientific.py
import numpy as np
from pytest import approx

from my_package.analysis import compute_mean, fit_linear

def test_compute_mean():
    """Test mean calculation."""
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = compute_mean(data)
    assert result == approx(3.0)

def test_fit_linear():
    """Test linear regression."""
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([0, 2, 4, 6, 8])
    slope, intercept = fit_linear(x, y)
    
    assert slope == approx(2.0)
    assert intercept == approx(0.0)
```

## Testing Best Practices

### Pattern 1: Writing Simple, Focused Tests

**Bad - Multiple assertions testing different things:**
```python
def test_everything():
    data = load_data("input.csv")
    assert len(data) > 0
    processed = process_data(data)
    assert processed.mean() > 0
    result = analyze(processed)
    assert result.success
```

**Good - Separate tests for each behavior:**
```python
def test_load_data_returns_nonempty():
    """Data loading should return at least one row."""
    data = load_data("input.csv")
    assert len(data) > 0

def test_process_data_positive_mean():
    """Processed data should have positive mean."""
    data = load_data("input.csv")
    processed = process_data(data)
    assert processed.mean() > 0

def test_analyze_succeeds():
    """Analysis should complete successfully."""
    data = load_data("input.csv")
    processed = process_data(data)
    result = analyze(processed)
    assert result.success
```

**Arrange-Act-Assert pattern:**
```python
def test_computation():
    # Arrange - Set up test data
    data = np.array([1, 2, 3, 4, 5])
    expected = 3.0
    
    # Act - Execute the function
    result = compute_mean(data)
    
    # Assert - Check the result
    assert result == approx(expected)
```

### Pattern 2: Testing for Failures

Always test that your code raises appropriate exceptions:

```python
import pytest

def test_zero_division_raises():
    """Division by zero should raise ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        result = 1 / 0

def test_invalid_input_raises():
    """Invalid input should raise ValueError."""
    with pytest.raises(ValueError, match="must be positive"):
        result = compute_sqrt(-1)

def test_deprecation_warning():
    """Deprecated function should warn."""
    with pytest.warns(DeprecationWarning):
        result = old_function()

def test_deprecated_call():
    """Check for deprecated API usage."""
    with pytest.deprecated_call():
        result = legacy_api()
```

### Pattern 3: Approximate Comparisons

Scientific computing often involves floating-point arithmetic that cannot be tested for exact equality:

**For scalars:**
```python
from pytest import approx

def test_approximate_scalar():
    """Test with approximate comparison."""
    result = 1 / 3
    assert result == approx(0.33333333333, rel=1e-10)
    
    # Default relative tolerance is 1e-6
    assert 0.3 + 0.3 == approx(0.6)

def test_approximate_with_absolute_tolerance():
    """Test with absolute tolerance."""
    result = compute_small_value()
    assert result == approx(0.0, abs=1e-10)
```

**For NumPy arrays (preferred over numpy.testing):**
```python
import numpy as np
from pytest import approx

def test_array_approximate():
    """Test NumPy arrays with approx."""
    result = np.array([0.1, 0.2, 0.3])
    expected = np.array([0.10001, 0.20001, 0.30001])
    assert result == approx(expected)

def test_array_with_nan():
    """Handle NaN values in arrays."""
    result = np.array([1.0, np.nan, 3.0])
    expected = np.array([1.0, np.nan, 3.0])
    assert result == approx(expected, nan_ok=True)
```

**When to use numpy.testing:**
```python
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def test_exact_integer_array():
    """Use numpy.testing for exact integer comparisons."""
    result = np.array([1, 2, 3])
    expected = np.array([1, 2, 3])
    assert_array_equal(result, expected)

def test_complex_array_tolerances():
    """Use numpy.testing for complex tolerance requirements."""
    result = compute_result()
    expected = load_reference()
    assert_allclose(result, expected, rtol=1e-7, atol=1e-10)
```

### Pattern 4: Using Fixtures

Fixtures provide reusable test setup and teardown:

**Basic fixtures:**
```python
import pytest
import numpy as np

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return np.array([1.0, 2.0, 3.0, 4.0, 5.0])

@pytest.fixture
def empty_array():
    """Provide empty array for edge case tests."""
    return np.array([])

def test_mean_with_fixture(sample_data):
    """Test using fixture."""
    result = np.mean(sample_data)
    assert result == approx(3.0)

def test_empty_array(empty_array):
    """Test edge case with empty array."""
    with pytest.warns(RuntimeWarning):
        result = np.mean(empty_array)
        assert np.isnan(result)
```

**Fixtures with setup and teardown:**
```python
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_datafile():
    """Create temporary data file for tests."""
    # Setup
    tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    tmpfile.write("1.0\n2.0\n3.0\n")
    tmpfile.close()
    
    # Provide to test
    yield Path(tmpfile.name)
    
    # Teardown
    Path(tmpfile.name).unlink()

def test_load_data(temp_datafile):
    """Test data loading from file."""
    data = np.loadtxt(temp_datafile)
    assert len(data) == 3
    assert data[0] == approx(1.0)
```

**Fixture scopes:**
```python
@pytest.fixture(scope="function")  # Default, run for each test
def data_per_test():
    return create_data()

@pytest.fixture(scope="class")  # Run once per test class
def data_per_class():
    return create_data()

@pytest.fixture(scope="module")  # Run once per module
def data_per_module():
    return load_large_dataset()

@pytest.fixture(scope="session")  # Run once per test session
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

**Auto-use fixtures:**
```python
@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seed before each test for reproducibility."""
    np.random.seed(42)
```

### Pattern 5: Parametrized Tests

Test the same function with multiple inputs:

**Basic parametrization:**
```python
import pytest

@pytest.mark.parametrize("input_val,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (-2, 4),
])
def test_square(input_val, expected):
    """Test squaring with multiple inputs."""
    assert input_val**2 == expected

@pytest.mark.parametrize("angle", [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
def test_sine_range(angle):
    """Test sine function returns values in [0, 1] for first quadrant."""
    result = np.sin(angle)
    assert 0 <= result <= 1
```

**Multiple parameters:**
```python
@pytest.mark.parametrize("n_air,n_water", [
    (1.0, 1.33),
    (1.0, 1.5),
    (1.5, 1.0),
])
def test_refraction(n_air, n_water):
    """Test Snell's law with different refractive indices."""
    angle_in = np.pi / 4
    angle_out = snell(angle_in, n_air, n_water)
    assert angle_out >= 0
    assert angle_out <= np.pi / 2
```

**Parametrized fixtures:**
```python
@pytest.fixture(params=[1, 2, 3], ids=["one", "two", "three"])
def dimension(request):
    """Parametrized fixture for different dimensions."""
    return request.param

def test_array_creation(dimension):
    """Test array creation in different dimensions."""
    shape = tuple([10] * dimension)
    arr = np.zeros(shape)
    assert arr.ndim == dimension
    assert arr.shape == shape
```

**Combining parametrization with custom IDs:**
```python
@pytest.mark.parametrize(
    "data,expected",
    [
        (np.array([1, 2, 3]), 2.0),
        (np.array([1, 1, 1]), 1.0),
        (np.array([0, 10]), 5.0),
    ],
    ids=["sequential", "constant", "extremes"]
)
def test_mean_with_ids(data, expected):
    """Test mean with descriptive test IDs."""
    assert np.mean(data) == approx(expected)
```

### Pattern 6: Test Organization with Markers

Use markers to organize and selectively run tests:

**Basic markers:**
```python
import pytest

@pytest.mark.slow
def test_expensive_computation():
    """Test that takes a long time."""
    result = run_simulation(n_iterations=1000000)
    assert result.converged

@pytest.mark.requires_gpu
def test_gpu_acceleration():
    """Test that requires GPU hardware."""
    result = compute_on_gpu(large_array)
    assert result.success

@pytest.mark.integration
def test_full_pipeline():
    """Integration test for complete workflow."""
    data = load_data()
    processed = preprocess(data)
    result = analyze(processed)
    output = save_results(result)
    assert output.exists()
```

**Running specific markers:**
```bash
pytest -m slow              # Run only slow tests
pytest -m "not slow"        # Skip slow tests
pytest -m "slow or gpu"     # Run slow OR gpu tests
pytest -m "slow and integration"  # Run slow AND integration tests
```

**Skip and xfail markers:**
```python
@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Test for feature under development."""
    result = future_function()
    assert result.success

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_pattern_matching():
    """Test using Python 3.10+ features."""
    match value:
        case 0:
            result = "zero"
        case _:
            result = "other"
    assert result == "zero"

@pytest.mark.xfail(reason="Known bug in upstream library")
def test_known_failure():
    """Test that currently fails due to known issue."""
    result = buggy_function()
    assert result == expected

@pytest.mark.xfail(strict=True)
def test_must_fail():
    """Test that MUST fail (test will fail if it passes)."""
    with pytest.raises(NotImplementedError):
        unimplemented_function()
```

**Custom markers in pyproject.toml:**
```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "requires_gpu: marks tests that need GPU hardware",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

### Pattern 6b: Organizing Test Suites by Directory

Following [Scientific Python recommendations](https://learn.scientific-python.org/development/principles/testing/#test-suites), organize tests into separate directories by type and execution time:

```text
tests/
├── unit/               # Fast, isolated unit tests
│   ├── conftest.py
│   ├── test_analysis.py
│   └── test_utils.py
├── integration/        # Integration tests
│   ├── conftest.py
│   └── test_pipeline.py
├── e2e/               # End-to-end tests
│   └── test_workflows.py
└── conftest.py        # Shared fixtures
```

**Run specific test suites:**
```bash
# Run only unit tests (fast)
pytest tests/unit/

# Run integration tests after unit tests pass
pytest tests/integration/

# Run all tests
pytest
```

**Auto-mark all tests in a directory using conftest.py:**
```python
# tests/unit/conftest.py
import pytest

def pytest_collection_modifyitems(session, config, items):
    """Automatically mark all tests in this directory as unit tests."""
    for item in items:
        item.add_marker(pytest.mark.unit)
```

**Benefits of organized test suites:**
- Run fast tests first ("fail fast" principle)
- Developers can run relevant tests quickly
- Clear separation of test types
- Avoid false positives from slow/flaky tests
- Better CI/CD optimization

**Example test runner strategy:**
```bash
# Run fast unit tests first, stop on failure
pytest tests/unit/ -x || exit 1

# If unit tests pass, run integration tests
pytest tests/integration/ -x || exit 1

# Finally run slow end-to-end tests
pytest tests/e2e/
```

### Pattern 7: Mocking and Monkeypatching

Mock expensive operations or external dependencies:

**Basic monkeypatching:**
```python
import platform

def test_platform_specific_behavior(monkeypatch):
    """Test behavior on different platforms."""
    # Mock platform.system() to return "Linux"
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    result = get_platform_specific_path()
    assert result == "/usr/local/data"
    
    # Change mock to return "Windows"
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    result = get_platform_specific_path()
    assert result == r"C:\Users\data"
```

**Mocking with pytest-mock:**
```python
import pytest
from unittest.mock import Mock

def test_expensive_computation(mocker):
    """Mock expensive computation."""
    # Mock the expensive function
    mock_compute = mocker.patch("my_package.analysis.expensive_compute")
    mock_compute.return_value = 42
    
    result = run_analysis()
    
    # Verify the mock was called
    mock_compute.assert_called_once()
    assert result == 42

def test_matplotlib_plotting(mocker):
    """Test plotting without creating actual plots."""
    mock_plt = mocker.patch("matplotlib.pyplot")
    
    create_plot(data)
    
    # Verify plot was created
    mock_plt.figure.assert_called_once()
    mock_plt.plot.assert_called_once()
    mock_plt.savefig.assert_called_once_with("output.png")
```

**Fixture for repeated mocking:**
```python
@pytest.fixture
def mock_matplotlib(mocker):
    """Mock matplotlib for testing plots."""
    fig = mocker.Mock(spec=plt.Figure)
    ax = mocker.Mock(spec=plt.Axes)
    line2d = mocker.Mock(name="plot", spec=plt.Line2D)
    ax.plot.return_value = (line2d,)
    
    mpl = mocker.patch("matplotlib.pyplot", autospec=True)
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig, ax))
    
    return {"fig": fig, "ax": ax, "mpl": mpl}

def test_my_plot(mock_matplotlib):
    """Test plotting function."""
    ax = mock_matplotlib["ax"]
    my_plotting_function(ax=ax)
    
    ax.plot.assert_called_once()
    ax.set_xlabel.assert_called_once()
```

### Pattern 8: Testing Against Installed Version

Always test the installed package, not local source:

**Why this matters:**
```
my-package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── data/            # Data files
│       │   └── reference.csv
│       └── analysis.py
└── tests/
    └── test_analysis.py
```

**Use src/ layout + editable install:**
```bash
# Install in editable mode
pip install -e .

# Run tests against installed version
pytest
```

**Benefits:**
- Tests ensure package installs correctly
- Catches missing files (like data files)
- Tests work in CI/CD environments
- Validates package structure and imports

**In tests, import from package:**
```python
# Good - imports installed package
from my_package.analysis import compute_mean

# Bad - would import from local src/ if not using src/ layout
# from analysis import compute_mean
```

### Pattern 8b: Import Best Practices in Tests

Following [Scientific Python unit testing guidelines](https://learn.scientific-python.org/development/principles/testing/#unit-tests), proper import patterns make tests more maintainable:

**Keep imports local to file under test:**
```python
# Good - Import from the file being tested
from my_package.analysis import MyClass, compute_mean

def test_compute_mean():
    """Test imports from module under test."""
    data = MyClass()
    result = compute_mean(data)
    assert result > 0
```

**Why this matters:**
- When code is refactored and symbols move, tests don't break
- Tests only care about symbols used in the file under test
- Reduces coupling between tests and internal code organization

**Import specific symbols, not entire modules:**
```python
# Good - Specific imports, easy to mock
from numpy import mean as np_mean, ndarray as NpArray

def my_function(data: NpArray) -> float:
    return np_mean(data)

# Good - Easy to patch in tests
def test_my_function(mocker):
    mock_mean = mocker.patch("my_package.analysis.np_mean")
    # ...
```

```python
# Less ideal - Harder to mock effectively
import numpy as np

def my_function(data: np.ndarray) -> float:
    return np.mean(data)

# Less ideal - Complex patching required
def test_my_function(mocker):
    # Must patch through the aliased namespace
    mock_mean = mocker.patch("my_package.analysis.np.mean")
    # ...
```

**Consider meaningful aliases:**
```python
# Make imports meaningful to your domain
from numpy import sum as numeric_sum
from scipy.stats import ttest_ind as statistical_test

# Easy to understand and replace
result = numeric_sum(values)
p_value = statistical_test(group1, group2)
```

This approach makes it easier to:
- Replace implementations without changing tests
- Mock dependencies effectively
- Understand code purpose from import names

## Running pytest

### Basic Usage

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_analysis.py

# Run specific test
pytest tests/test_analysis.py::test_mean

# Run tests matching pattern
pytest -k "mean or median"

# Verbose output
pytest -v

# Show local variables in failures
pytest -l  # or --showlocals

# Stop at first failure
pytest -x

# Show stdout/stderr
pytest -s
```

### Debugging Tests

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of each test
pytest --trace

# Run last failed tests
pytest --lf

# Run failed tests first, then rest
pytest --ff

# Show which tests would be run (dry run)
pytest --collect-only
```

### Coverage

```bash
# Install pytest-cov
pip install pytest-cov

# Run with coverage
pytest --cov=my_package

# With coverage report
pytest --cov=my_package --cov-report=html

# With missing lines
pytest --cov=my_package --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=my_package --cov-fail-under=90
```

**Configure in pyproject.toml:**
```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=my_package",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]
```

## Scientific Python Testing Patterns

### Pattern 9: Testing Numerical Algorithms

```python
import numpy as np
from pytest import approx

def test_numerical_stability():
    """Test algorithm is numerically stable."""
    data = np.array([1e10, 1.0, -1e10])
    result = stable_sum(data)
    assert result == approx(1.0)

def test_convergence():
    """Test iterative algorithm converges."""
    x0 = np.array([1.0, 1.0, 1.0])
    result = iterative_solver(x0, tol=1e-8, max_iter=1000)
    
    assert result.converged
    assert result.iterations < 1000
    assert result.residual < 1e-8

def test_against_analytical_solution():
    """Test against known analytical result."""
    x = np.linspace(0, 1, 100)
    numerical = compute_integral(lambda t: t**2, x)
    analytical = x**3 / 3
    assert numerical == approx(analytical, rel=1e-6)

def test_conservation_law():
    """Test that physical conservation law holds."""
    initial_energy = compute_energy(system)
    system.evolve(dt=0.01, steps=1000)
    final_energy = compute_energy(system)
    
    # Energy should be conserved (within numerical error)
    assert final_energy == approx(initial_energy, rel=1e-10)
```

### Pattern 10: Testing with Different NumPy dtypes

```python
@pytest.mark.parametrize("dtype", [
    np.float32,
    np.float64,
    np.complex64,
    np.complex128,
])
def test_computation_dtypes(dtype):
    """Test function works with different dtypes."""
    data = np.array([1, 2, 3, 4, 5], dtype=dtype)
    result = compute_transform(data)
    
    assert result.dtype == dtype
    assert result.shape == data.shape

@pytest.mark.parametrize("dtype", [np.int32, np.int64, np.float32, np.float64])
def test_integer_and_float_types(dtype):
    """Test handling of integer and float types."""
    arr = np.array([1, 2, 3], dtype=dtype)
    result = safe_divide(arr, 2)
    
    # Result should be floating point
    assert result.dtype in [np.float32, np.float64]
```

### Pattern 11: Testing Random/Stochastic Code

```python
def test_random_with_seed():
    """Test random code with fixed seed for reproducibility."""
    np.random.seed(42)
    result1 = generate_random_samples(n=100)
    
    np.random.seed(42)
    result2 = generate_random_samples(n=100)
    
    # Should get identical results with same seed
    assert np.array_equal(result1, result2)

def test_statistical_properties():
    """Test statistical properties of random output."""
    np.random.seed(123)
    samples = generate_normal_samples(n=100000, mean=0, std=1)
    
    # Test mean and std are close to expected (not exact due to randomness)
    assert np.mean(samples) == approx(0, abs=0.01)
    assert np.std(samples) == approx(1, abs=0.01)

@pytest.mark.parametrize("seed", [42, 123, 456])
def test_reproducibility_with_seeds(seed):
    """Test reproducibility with different seeds."""
    np.random.seed(seed)
    result = stochastic_algorithm()
    
    # Should complete successfully regardless of seed
    assert result.success
```

### Pattern 12: Testing Data Pipelines

```python
def test_pipeline_end_to_end(tmp_path):
    """Test complete data pipeline."""
    # Arrange - Create input data
    input_file = tmp_path / "input.csv"
    input_file.write_text("x,y\n1,2\n3,4\n5,6\n")
    
    output_file = tmp_path / "output.csv"
    
    # Act - Run pipeline
    result = run_pipeline(input_file, output_file)
    
    # Assert - Check results
    assert result.success
    assert output_file.exists()
    
    output_data = np.loadtxt(output_file, delimiter=",", skiprows=1)
    assert len(output_data) == 3

def test_pipeline_stages_independently():
    """Test each pipeline stage separately."""
    # Test stage 1
    raw_data = load_data("input.csv")
    assert len(raw_data) > 0
    
    # Test stage 2
    cleaned = clean_data(raw_data)
    assert not np.any(np.isnan(cleaned))
    
    # Test stage 3
    transformed = transform_data(cleaned)
    assert transformed.shape == cleaned.shape
    
    # Test stage 4
    result = analyze_data(transformed)
    assert result.metrics["r2"] > 0.9
```

### Pattern 13: Property-Based Testing with Hypothesis

For complex scientific code, consider property-based testing:

```python
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays
import numpy as np

@given(arrays(np.float64, shape=st.integers(1, 100)))
def test_mean_is_bounded(arr):
    """Mean should be between min and max."""
    if len(arr) > 0 and not np.any(np.isnan(arr)):
        mean = np.mean(arr)
        assert np.min(arr) <= mean <= np.max(arr)

@given(
    x=arrays(np.float64, shape=10, elements=st.floats(-100, 100)),
    y=arrays(np.float64, shape=10, elements=st.floats(-100, 100))
)
def test_linear_fit_properties(x, y):
    """Test properties of linear regression."""
    if not (np.any(np.isnan(x)) or np.any(np.isnan(y))):
        slope, intercept = fit_linear(x, y)
        
        # Predictions should be finite
        predictions = slope * x + intercept
        assert np.all(np.isfinite(predictions))
```

## Test Configuration Examples

### Complete pyproject.toml Testing Section

```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = [
    "-ra",                          # Show summary of all test outcomes
    "--showlocals",                 # Show local variables in tracebacks
    "--strict-markers",             # Error on undefined markers
    "--strict-config",              # Error on config issues
    "--cov=my_package",             # Coverage for package
    "--cov-report=term-missing",    # Show missing lines
    "--cov-report=html",            # HTML coverage report
]
xfail_strict = true                 # xfail tests must fail
filterwarnings = [
    "error",                        # Treat warnings as errors
    "ignore::DeprecationWarning:pkg_resources",  # Ignore specific warning
    "ignore::PendingDeprecationWarning",
]
log_cli_level = "info"              # Log level for test output
testpaths = [
    "tests",                        # Test directory
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "requires_gpu: marks tests that need GPU hardware",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]
branch = true                       # Measure branch coverage

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]
precision = 2
show_missing = true
skip_covered = false
```

### conftest.py for Shared Fixtures

```python
# tests/conftest.py
import pytest
import numpy as np
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "data"

@pytest.fixture
def sample_array():
    """Provide sample NumPy array."""
    np.random.seed(42)
    return np.random.randn(100)

@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide temporary directory for test outputs."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir

@pytest.fixture(autouse=True)
def reset_random_state():
    """Reset random state before each test."""
    np.random.seed(42)

@pytest.fixture(scope="session")
def large_dataset():
    """Load large dataset once per test session."""
    return load_reference_data()

# Platform-specific fixtures
@pytest.fixture(params=["Linux", "Darwin", "Windows"])
def platform_name(request, monkeypatch):
    """Parametrize tests across platforms."""
    monkeypatch.setattr("platform.system", lambda: request.param)
    return request.param
```

## Common Testing Pitfalls and Solutions

### Pitfall 1: Testing Implementation Instead of Behavior

**Bad:**
```python
def test_uses_numpy_mean():
    """Test that function uses np.mean."""  # Testing implementation!
    # This is fragile - breaks if implementation changes
    pass
```

**Good:**
```python
def test_computes_correct_average():
    """Test that function returns correct average."""
    data = np.array([1, 2, 3, 4, 5])
    result = compute_average(data)
    assert result == approx(3.0)
```

### Pitfall 2: Non-Deterministic Tests

**Bad:**
```python
def test_random_sampling():
    samples = generate_samples()  # Uses random seed from system time!
    assert samples[0] > 0  # Might fail randomly
```

**Good:**
```python
def test_random_sampling():
    np.random.seed(42)  # Fixed seed
    samples = generate_samples()
    assert samples[0] == approx(0.4967, rel=1e-4)
```

### Pitfall 3: Exact Floating-Point Comparisons

**Bad:**
```python
def test_computation():
    result = 0.1 + 0.2
    assert result == 0.3  # Fails due to floating-point error!
```

**Good:**
```python
def test_computation():
    result = 0.1 + 0.2
    assert result == approx(0.3)
```

### Pitfall 4: Testing Too Much in One Test

**Bad:**
```python
def test_entire_analysis():
    # Load data
    data = load_data()
    assert data is not None
    
    # Process
    processed = process(data)
    assert len(processed) > 0
    
    # Analyze
    result = analyze(processed)
    assert result.score > 0.8
    
    # Save
    save_results(result, "output.txt")
    assert Path("output.txt").exists()
```

**Good:**
```python
def test_load_data_succeeds():
    data = load_data()
    assert data is not None

def test_process_returns_nonempty():
    data = load_data()
    processed = process(data)
    assert len(processed) > 0

def test_analyze_gives_good_score():
    data = load_data()
    processed = process(data)
    result = analyze(processed)
    assert result.score > 0.8

def test_save_results_creates_file(tmp_path):
    output_file = tmp_path / "output.txt"
    result = create_mock_result()
    save_results(result, output_file)
    assert output_file.exists()
```

## Testing Checklist

- [ ] Tests are in `tests/` directory separate from source
- [ ] Test files named `test_*.py`
- [ ] Test functions named `test_*`
- [ ] Tests run against installed package (use src/ layout)
- [ ] pytest configured in `pyproject.toml`
- [ ] Using `pytest.approx` for floating-point comparisons
- [ ] Tests check exceptions with `pytest.raises`
- [ ] Tests check warnings with `pytest.warns`
- [ ] Parametrized tests for multiple inputs
- [ ] Fixtures for reusable setup
- [ ] Markers used for test organization
- [ ] Random tests use fixed seeds
- [ ] Tests are independent (can run in any order)
- [ ] Each test focuses on one behavior
- [ ] Coverage > 80% (preferably > 90%)
- [ ] All tests pass before committing
- [ ] Slow tests marked with `@pytest.mark.slow`
- [ ] Integration tests marked appropriately
- [ ] CI configured to run tests automatically

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          pytest --cov=my_package --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

## Resources

- **Scientific Python pytest Guide**: <https://learn.scientific-python.org/development/guides/pytest/>
- **Scientific Python Testing Tutorial**: <https://learn.scientific-python.org/development/tutorials/test/>
- **Scientific Python Testing Principles**: <https://learn.scientific-python.org/development/principles/testing/>
- **pytest Documentation**: <https://docs.pytest.org/>
- **pytest-cov**: <https://pytest-cov.readthedocs.io/>
- **pytest-mock**: <https://pytest-mock.readthedocs.io/>
- **Hypothesis (property-based testing)**: <https://hypothesis.readthedocs.io/>
- **NumPy testing utilities**: <https://numpy.org/doc/stable/reference/routines.testing.html>
- **Testing best practices**: <https://docs.python-guide.org/writing/tests/>

## Summary

Testing scientific Python code with pytest, following Scientific Python community principles, provides:

1. **Confidence**: Know your code works correctly
2. **Reproducibility**: Ensure consistent behavior across environments
3. **Documentation**: Tests show how code should be used and communicate developer intent
4. **Refactoring safety**: Change code without breaking functionality
5. **Regression prevention**: Catch bugs before they reach users
6. **Scientific rigor**: Validate numerical accuracy and physical correctness

**Key testing principles:**

- Start with **public interface tests** from the user's perspective
- Organize tests into **suites** (unit, integration, e2e) by type and speed
- Follow **outside-in** approach: public interface → integration → unit tests
- Keep tests **simple, focused, and independent**
- Test **behavior rather than implementation**
- Use pytest's powerful features (fixtures, parametrization, markers) effectively
- Always verify tests **fail when they should** to avoid false confidence

**Remember**: Any test is better than none, but well-organized tests following these principles create trustworthy, maintainable scientific software that the community can rely on.
