import numpy as np

def midpoint_rule(f, a, b, n):
    """Approximate integral of f on [a,b] using midpoint rule with n subintervals."""
    h = (b - a) / n
    xs = a + (np.arange(n) + 0.5) * h
    return h * np.sum(f(xs))

def trapezoid_rule(f, a, b, n):
    """Approximate integral of f on [a,b] using trapezoidal rule with n subintervals."""
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = f(xs)
    return (h / 2.0) * (ys[0] + 2.0 * np.sum(ys[1:-1]) + ys[-1])

def simpson_rule(f, a, b, n):
    """Approximate integral of f on [a,b] using Simpson's rule with n even subintervals."""
    if n % 2 != 0:
        raise ValueError("Simpson requires n to be even.")
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = f(xs)
    # 4 * odd indices, 2 * even (internal) indices
    return (h / 3.0) * (ys[0] + 4.0 * np.sum(ys[1:-1:2]) + 2.0 * np.sum(ys[2:-2:2]) + ys[-1])

# --------- Versions for tabulated/equally-spaced data ----------

def midpoint_from_samples(y, a, b):
    """
    Midpoint rule from equally spaced samples.
    y must be samples at midpoints between a and b with n entries.
    """
    n = len(y)
    h = (b - a) / n
    return h * float(np.sum(y))

def trapezoid_from_nodes(y, a, b):
    """
    Trapezoid rule from equally spaced node samples.
    y must be samples at the n+1 nodes on [a,b].
    """
    n = len(y) - 1
    h = (b - a) / n
    return (h / 2.0) * float(y[0] + 2.0 * np.sum(y[1:-1]) + y[-1])

def simpson_from_nodes(y, a, b):
    """
    Simpson rule from equally spaced node samples.
    y must be samples at the n+1 nodes on [a,b] with n even.
    """
    n = len(y) - 1
    if n % 2 != 0:
        raise ValueError("Simpson requires an even number of subintervals (len(y)-1 must be even).")
    h = (b - a) / n
    # indices: 0..n
    return (h / 3.0) * float(y[0] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-2:2]) + y[-1])

if __name__ == "__main__":
    # Small demo: integrate sqrt(2x+1) on [0,4] with n=4
    import math
    f = lambda x: np.sqrt(2*x + 1)
    a, b, n = 0.0, 4.0, 4

    print("Demo on f(x)=sqrt(2x+1) on [0,4], n=4")
    print("Midpoint:", midpoint_rule(f, a, b, n))
    print("Trapezoid:", trapezoid_rule(f, a, b, n))
    print("Simpson:", simpson_rule(f, a, b, n))
