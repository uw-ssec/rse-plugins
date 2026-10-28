#!/usr/bin/env bash
set -euo pipefail
mkdir -p /app/numlib/tests
cat > /app/numlib/tests/test_core.py <<'PY'
import numpy as np
import pytest
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays
from pytest import approx

from numlib import normalize, running_mean, trapezoid

finite = st.floats(-1e3, 1e3, allow_nan=False, allow_infinity=False)


class TestTrapezoid:
    def test_linear_is_exact(self):
        x = np.linspace(0.0, 2.0, 5)
        assert trapezoid(2 * x + 1, x) == approx(6.0)

    def test_quadratic_converges(self):
        x = np.linspace(0.0, 1.0, 1001)
        assert trapezoid(x**2, x) == approx(1 / 3, rel=1e-5)

    def test_reversed_x_flips_sign(self):
        x = np.linspace(0.0, 1.0, 11)
        assert trapezoid(x, x[::-1]) == approx(-0.5)

    def test_zero_integral_needs_abs_tolerance(self):
        x = np.linspace(-np.pi, np.pi, 2001)
        assert trapezoid(np.sin(x), x) == approx(0.0, abs=1e-12)

    @pytest.mark.parametrize("bad", [([1.0], [0.0]), ([1.0, 2.0], [0.0, 1.0, 2.0])])
    def test_invalid_input(self, bad):
        with pytest.raises(ValueError):
            trapezoid(*bad)


class TestNormalize:
    def test_known_values(self):
        np.testing.assert_allclose(normalize([2.0, 4.0, 6.0]), [0.0, 0.5, 1.0])

    def test_constant_maps_to_zeros(self):
        np.testing.assert_array_equal(normalize([3.0, 3.0]), [0.0, 0.0])

    @given(arrays(np.float64, st.integers(2, 50), elements=finite))
    def test_range_is_unit_interval(self, a):
        out = normalize(a)
        assert np.all(np.isfinite(out))
        assert out.min() == approx(0.0, abs=1e-12)
        if np.ptp(a) > 0:
            assert out.max() == approx(1.0)


class TestRunningMean:
    def test_known_values(self):
        np.testing.assert_allclose(running_mean([1.0, 2.0, 3.0, 4.0], 2), [1.5, 2.5, 3.5])

    @given(arrays(np.float64, st.integers(1, 40), elements=finite), st.data())
    def test_matches_convolution(self, a, data):
        w = data.draw(st.integers(1, a.size))
        expected = np.convolve(a, np.ones(w) / w, mode="valid")
        np.testing.assert_allclose(running_mean(a, w), expected, rtol=1e-9, atol=1e-9)

    @pytest.mark.parametrize("w", [0, 5])
    def test_bad_window(self, w):
        with pytest.raises(ValueError):
            running_mean([1.0, 2.0, 3.0], w)
PY
