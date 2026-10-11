from __future__ import annotations

from .curve import Curve


def f3(x1: int, x2: int, x3: int, curve: Curve) -> int:
    """Evaluate Semaev's third summation polynomial modulo ``curve.p``.

    For a short-Weierstrass curve, a zero means compatible y-coordinates exist
    over an algebraic closure such that the three associated points sum to zero.
    """

    p, a, b = curve.p, curve.a, curve.b
    x1, x2, x3 = x1 % p, x2 % p, x3 % p
    value = (
        (x1 - x2) ** 2 * x3**2
        - 2 * ((x1 + x2) * (x1 * x2 + a) + 2 * b) * x3
        + (x1 * x2 - a) ** 2
        - 4 * b * (x1 + x2)
    )
    return value % p


def single_coordinate_obstruction(
    x1: int, x2: int, x3: int, beta: int, curve: Curve
) -> int:
    """Return the nontrivial factor controlling ``x1 -> beta*x1`` for j=0.

    If ``a = 0`` and ``beta`` is a cube root of unity, then

    ``f3(beta*x1,x2,x3) - f3(x1,x2,x3)`` equals
    ``(beta-1)*x1*single_coordinate_obstruction(...)`` modulo ``p``.
    """

    if curve.a % curve.p != 0:
        raise ValueError("the obstruction identity requires a j=0 curve with a=0")
    p = curve.p
    x1, x2, x3, beta = x1 % p, x2 % p, x3 % p, beta % p
    if pow(beta, 3, p) != 1:
        raise ValueError("beta must be a cube root of unity")
    return (
        -4 * curve.b
        + (beta + 1) * x1 * (x2 - x3) ** 2
        - 2 * x2 * x3 * (x2 + x3)
    ) % p
