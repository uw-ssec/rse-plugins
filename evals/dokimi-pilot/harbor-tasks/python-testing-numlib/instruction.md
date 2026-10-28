# Test a small numerical library

`/app/numlib` is a scientific Python package (src layout) with three functions in
`src/numlib/core.py`: `trapezoid`, `normalize` and `running_mean`. It has no tests.

Write a pytest test suite for it in `/app/numlib/tests/`. The suite should:

- pass against the current implementation (run it with `cd /app/numlib && python -m pytest`);
- catch real bugs in these functions, including subtle numerical ones;
- use appropriate floating-point comparisons.

Don't modify `src/`. pytest, numpy and hypothesis are installed; there is no network access.
