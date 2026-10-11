from j0lab.curve import Curve, Point


def test_enumerated_points_are_on_curve() -> None:
    curve = Curve(p=31, a=0, b=7)

    points = curve.points()

    assert Point.infinity() in points
    assert len(points) > 1
    assert all(curve.contains(point) for point in points)


def test_group_operations_close_on_curve() -> None:
    curve = Curve(p=31, a=0, b=7)
    finite = [point for point in curve.points() if not point.is_infinity]
    left, right = finite[2], finite[7]

    total = curve.add(left, right)

    assert curve.contains(total)
    assert curve.add(left, curve.negate(left)).is_infinity
    assert curve.multiply(left, 0).is_infinity
    assert curve.multiply(left, 3) == curve.add(left, curve.add(left, left))


def test_nontrivial_cube_root_defines_j0_automorphism() -> None:
    curve = Curve(p=31, a=0, b=7)
    beta = curve.nontrivial_cube_root()
    point = next(point for point in curve.points() if not point.is_infinity and point.x != 0)

    rotated = curve.cubic_automorphism(point, beta)

    assert beta not in (0, 1)
    assert pow(beta, 3, curve.p) == 1
    assert curve.contains(rotated)
    assert curve.cubic_automorphism(rotated, beta) != point
    assert curve.cubic_automorphism(curve.cubic_automorphism(rotated, beta), beta) == point
