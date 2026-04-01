---
description: Write or improve pytest tests for scientific Python code with fixtures, parametrization, and numerical testing patterns
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Python Testing

Write or improve tests for scientific Python code using pytest.

## Arguments

$ARGUMENTS — optional target (e.g., "test the transform module", "add parametrized tests for edge cases", "set up pytest config")

## Workflow

1. **Explore the project** to understand what needs testing:
   - Find source modules and their public API
   - Check for existing tests in `tests/` or `test_*.py`
   - Read `pyproject.toml` for pytest configuration

2. **Determine the task** based on arguments:
   - **New tests**: create test files following existing structure
   - **Improve coverage**: identify untested functions and add tests
   - **Configure**: set up pytest in pyproject.toml with markers, fixtures, coverage

3. **Apply scientific testing patterns:**
   - Outside-in testing (public API first)
   - NumPy testing utilities for numerical comparisons (`np.testing.assert_allclose`)
   - Proper tolerances for floating-point comparisons
   - Fixtures for test data and temporary files
   - Parametrize across edge cases (NaN, inf, empty arrays, boundary values)
   - Property-based testing with Hypothesis where appropriate

4. **Run the tests** to verify they pass:
   ```bash
   pytest -x -v <test_file>
   ```

5. **Report** what was tested and any gaps remaining.
