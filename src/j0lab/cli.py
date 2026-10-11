from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from .experiment import analyze_curve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare cube-root actions on j=0 and matched toy-field control curves."
    )
    parser.add_argument(
        "--primes",
        nargs="+",
        type=int,
        default=[19, 31, 37, 43, 61],
        help="small primes congruent to 1 modulo 3",
    )
    parser.add_argument("--b", type=int, default=7)
    parser.add_argument("--control-a", type=int, default=2)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    invalid = [prime for prime in args.primes if prime % 3 != 1]
    if invalid:
        raise SystemExit(f"primes must be 1 modulo 3; received {invalid}")
    j0_controls = [prime for prime in args.primes if args.control_a % prime == 0]
    if j0_controls:
        raise SystemExit(
            "control-a must be nonzero in every selected field; "
            f"zero modulo {j0_controls}"
        )

    experiments = []
    for prime in args.primes:
        j0 = analyze_curve(p=prime, a=0, b=args.b)
        control = analyze_curve(p=prime, a=args.control_a, b=args.b)
        experiments.append({"j0": j0.as_dict(), "control": control.as_dict()})

    payload = {
        "schema_version": 1,
        "description": "toy-field Semaev-f3 cube-root symmetry comparison",
        "experiments": experiments,
    }
    print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
