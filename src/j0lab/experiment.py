from __future__ import annotations

from dataclasses import asdict, dataclass

from .curve import Curve
from .semaev import f3, single_coordinate_obstruction


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    p: int
    a: int
    b: int
    point_count: int
    beta: int
    relation_count: int
    diagonal_preserved: int
    single_coordinate_preserved: int
    single_preserved_x1_zero: int
    single_preserved_obstruction_zero: int
    single_preserved_unexplained: int | None

    @property
    def diagonal_rate(self) -> float:
        return self.diagonal_preserved / self.relation_count

    @property
    def single_coordinate_rate(self) -> float:
        return self.single_coordinate_preserved / self.relation_count

    def as_dict(self) -> dict[str, int | float | None]:
        payload = asdict(self)
        payload["diagonal_rate"] = self.diagonal_rate
        payload["single_coordinate_rate"] = self.single_coordinate_rate
        return payload


def analyze_curve(*, p: int, a: int, b: int) -> ExperimentResult:
    """Measure how x-coordinate cube-root actions affect rational f3 relations."""

    curve = Curve(p=p, a=a, b=b)
    beta = curve.nontrivial_cube_root()
    finite = [point for point in curve.points() if not point.is_infinity]
    relation_count = 0
    diagonal_preserved = 0
    single_coordinate_preserved = 0
    single_preserved_x1_zero = 0
    single_preserved_obstruction_zero = 0
    single_preserved_unexplained = 0 if a == 0 else None

    for left in finite:
        for right in finite:
            third = curve.negate(curve.add(left, right))
            if third.is_infinity:
                continue
            assert left.x is not None and right.x is not None and third.x is not None
            if f3(left.x, right.x, third.x, curve) != 0:
                raise AssertionError("group relation did not satisfy f3")

            relation_count += 1
            if f3(beta * left.x, beta * right.x, beta * third.x, curve) == 0:
                diagonal_preserved += 1
            if f3(beta * left.x, right.x, third.x, curve) == 0:
                single_coordinate_preserved += 1
                if left.x == 0:
                    single_preserved_x1_zero += 1
                if a == 0:
                    obstruction_is_zero = single_coordinate_obstruction(
                        left.x, right.x, third.x, beta, curve
                    ) == 0
                    if obstruction_is_zero:
                        single_preserved_obstruction_zero += 1
                    if left.x != 0 and not obstruction_is_zero:
                        assert single_preserved_unexplained is not None
                        single_preserved_unexplained += 1

    if relation_count == 0:
        raise ValueError("curve produced no finite rational relations")
    return ExperimentResult(
        p=p,
        a=a,
        b=b,
        point_count=len(finite) + 1,
        beta=beta,
        relation_count=relation_count,
        diagonal_preserved=diagonal_preserved,
        single_coordinate_preserved=single_coordinate_preserved,
        single_preserved_x1_zero=single_preserved_x1_zero,
        single_preserved_obstruction_zero=single_preserved_obstruction_zero,
        single_preserved_unexplained=single_preserved_unexplained,
    )
