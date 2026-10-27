import numpy as np


def trapezoid(y, x):
    """Integrate samples y(x) with the composite trapezoidal rule."""
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    if y.shape != x.shape or y.ndim != 1:
        raise ValueError("x and y must be 1-D arrays of the same length")
    if y.size < 2:
        raise ValueError("need at least two samples")
    return float(np.sum((x[1:] - x[:-1]) * (y[1:] + y[:-1]) / 2.0))


def normalize(a):
    """Rescale a to [0, 1]. A constant array maps to zeros."""
    a = np.asarray(a, dtype=float)
    span = a.max() - a.min()
    return (a - a.min()) / span


def running_mean(a, window):
    """Mean over each full window of length `window` (valid mode)."""
    a = np.asarray(a, dtype=float)
    if not 1 <= window <= a.size:
        raise ValueError("window must be between 1 and len(a)")
    c = np.cumsum(np.insert(a, 0, 0.0))
    return (c[window:] - c[:-window]) / window
