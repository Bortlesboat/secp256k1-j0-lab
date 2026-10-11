from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    x: int | None
    y: int | None

    @classmethod
    def infinity(cls) -> Point:
        return cls(None, None)

    @property
    def is_infinity(self) -> bool:
        return self.x is None and self.y is None


@dataclass(frozen=True, slots=True)
class Curve:
    """A short-Weierstrass curve over a small prime field.

    The implementation is intentionally simple and auditable. It is for generated
    toy-field experiments, not production cryptography.
    """

    p: int
    a: int
    b: int

    def __post_init__(self) -> None:
        if self.p <= 3 or not _is_prime(self.p):
            raise ValueError("p must be a prime greater than 3")
        if (4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)) % self.p == 0:
            raise ValueError("curve must be nonsingular")

    def contains(self, point: Point) -> bool:
        if point.is_infinity:
            return True
        if point.x is None or point.y is None:
            return False
        x, y = point.x % self.p, point.y % self.p
        return y * y % self.p == (x * x * x + self.a * x + self.b) % self.p

    def points(self) -> tuple[Point, ...]:
        points = [Point.infinity()]
        for x in range(self.p):
            rhs = (x * x * x + self.a * x + self.b) % self.p
            for y in range(self.p):
                if y * y % self.p == rhs:
                    points.append(Point(x, y))
        return tuple(points)

    def negate(self, point: Point) -> Point:
        self._require_point(point)
        if point.is_infinity:
            return point
        assert point.x is not None and point.y is not None
        return Point(point.x % self.p, (-point.y) % self.p)

    def add(self, left: Point, right: Point) -> Point:
        self._require_point(left)
        self._require_point(right)
        if left.is_infinity:
            return right
        if right.is_infinity:
            return left

        assert left.x is not None and left.y is not None
        assert right.x is not None and right.y is not None
        if left.x == right.x and (left.y + right.y) % self.p == 0:
            return Point.infinity()

        if left == right:
            slope = (3 * left.x * left.x + self.a) * pow(2 * left.y, -1, self.p)
        else:
            slope = (right.y - left.y) * pow(right.x - left.x, -1, self.p)
        slope %= self.p

        x = (slope * slope - left.x - right.x) % self.p
        y = (slope * (left.x - x) - left.y) % self.p
        result = Point(x, y)
        self._require_point(result)
        return result

    def multiply(self, point: Point, scalar: int) -> Point:
        self._require_point(point)
        if scalar < 0:
            return self.multiply(self.negate(point), -scalar)

        result = Point.infinity()
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def nontrivial_cube_root(self) -> int:
        for candidate in range(2, self.p):
            if pow(candidate, 3, self.p) == 1:
                return candidate
        raise ValueError("field has no nontrivial cube root of unity")

    def cubic_automorphism(self, point: Point, beta: int | None = None) -> Point:
        if self.a % self.p != 0:
            raise ValueError("the cubic automorphism requires a j=0 curve with a=0")
        self._require_point(point)
        if point.is_infinity:
            return point
        beta = self.nontrivial_cube_root() if beta is None else beta % self.p
        if beta == 1 or pow(beta, 3, self.p) != 1:
            raise ValueError("beta must be a nontrivial cube root of unity")
        assert point.x is not None and point.y is not None
        result = Point(beta * point.x % self.p, point.y)
        self._require_point(result)
        return result

    def _require_point(self, point: Point) -> None:
        if not self.contains(point):
            raise ValueError("point is not on this curve")


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True
