from j0lab.curve import Curve
from j0lab.semaev import f3, single_coordinate_obstruction


def _nondegenerate_relation(curve: Curve):
    finite = [point for point in curve.points() if not point.is_infinity]
    for left in finite:
        for right in finite:
            third = curve.negate(curve.add(left, right))
            if not third.is_infinity and len({left.x, right.x, third.x}) == 3:
                return left, right, third
    raise AssertionError("curve did not provide a nondegenerate relation")


def test_f3_vanishes_for_three_points_summing_to_infinity() -> None:
    curve = Curve(p=31, a=0, b=7)
    left, right, third = _nondegenerate_relation(curve)

    assert curve.add(curve.add(left, right), third).is_infinity
    assert f3(left.x, right.x, third.x, curve) == 0


def test_j0_diagonal_automorphism_is_a_semi_invariance() -> None:
    curve = Curve(p=13, a=0, b=7)
    beta = curve.nontrivial_cube_root()

    for x1 in range(curve.p):
        for x2 in range(curve.p):
            for x3 in range(curve.p):
                rotated = f3(beta * x1, beta * x2, beta * x3, curve)

                assert rotated == beta * f3(x1, x2, x3, curve) % curve.p


def test_independent_coordinate_rotation_does_not_preserve_all_relations() -> None:
    curve = Curve(p=31, a=0, b=7)
    beta = curve.nontrivial_cube_root()
    finite = [point for point in curve.points() if not point.is_infinity]

    counterexamples = []
    for left in finite:
        for right in finite:
            third = curve.negate(curve.add(left, right))
            if third.is_infinity or len({left.x, right.x, third.x}) < 3:
                continue
            if f3(beta * left.x, right.x, third.x, curve) != 0:
                counterexamples.append((left, right, third))

    assert counterexamples


def test_generic_curve_lacks_j0_diagonal_semi_invariance() -> None:
    curve = Curve(p=31, a=2, b=7)
    beta = curve.nontrivial_cube_root()
    x1, x2, x3 = 3, 11, 19

    rotated = f3(beta * x1, beta * x2, beta * x3, curve)

    assert rotated != beta * f3(x1, x2, x3, curve) % curve.p


def test_single_coordinate_rotation_has_an_explicit_obstruction() -> None:
    curve = Curve(p=13, a=0, b=7)
    beta = curve.nontrivial_cube_root()

    for x1 in range(curve.p):
        for x2 in range(curve.p):
            for x3 in range(curve.p):
                observed_delta = (
                    f3(beta * x1, x2, x3, curve) - f3(x1, x2, x3, curve)
                ) % curve.p
                predicted_delta = (
                    (beta - 1)
                    * x1
                    * single_coordinate_obstruction(x1, x2, x3, beta, curve)
                ) % curve.p

                assert observed_delta == predicted_delta
