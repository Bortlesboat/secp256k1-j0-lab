# Diagonal cube-root symmetry of the third summation polynomial

Date: 2026-10-10

## Question

For a prime field with a nontrivial cube root of unity, does the extra
automorphism of a `j = 0` curve create an independently usable symmetry in the
third Semaev summation polynomial, or only a global diagonal symmetry?

This is relevant to algebraic discrete-logarithm research because a symmetry
that acts independently on factor-base coordinates could reduce relation-search
or polynomial-solving costs. A symmetry that acts only diagonally identifies a
constant-size global orbit and does not by itself provide that reduction.

## Setup

Let

```text
E / F_p: y^2 = x^3 + b,
```

where `p > 3`, `b != 0`, and `p = 1 mod 3`. Choose `beta` in `F_p` such that
`beta^3 = 1` and `beta != 1`. Then

```text
phi(x, y) = (beta*x, y)
```

is an order-three automorphism of `E`.

For a short-Weierstrass curve `y^2 = x^3 + a*x + b`, the third summation
polynomial used here is

```text
f3(x1,x2,x3) =
    (x1-x2)^2*x3^2
  - 2*((x1+x2)*(x1*x2+a) + 2*b)*x3
  + (x1*x2-a)^2
  - 4*b*(x1+x2).
```

All equalities below are in `F_p`.

## Proposition

When `a = 0`,

```text
f3(beta*x1, beta*x2, beta*x3) = beta*f3(x1,x2,x3).
```

Therefore the zero set of `f3` is invariant under the diagonal action
`(x1,x2,x3) -> (beta*x1,beta*x2,beta*x3)`.

### Direct verification

Every term in `f3` has weight one modulo three when each `xi` is assigned
weight one:

- `(x1-x2)^2*x3^2` has total weight four, hence scales by `beta^4 = beta`.
- `(x1+x2)*x1*x2*x3` also has total weight four.
- `b*x3` and `b*(x1+x2)` have weight one.
- `(x1*x2)^2` has total weight four.

Thus the complete polynomial scales by `beta`. This is a semi-invariance, and
its zero set is invariant.

For one-coordinate rotation, direct subtraction and factorization give the
stronger identity

```text
f3(beta*x1,x2,x3) - f3(x1,x2,x3)
  = (beta-1)*x1*g_beta(x1,x2,x3),

g_beta(x1,x2,x3)
  = -4*b
    + (beta+1)*x1*(x2-x3)^2
    - 2*x2*x3*(x2+x3).
```

Consequently, a relation survives this one-coordinate rotation only when
`x1 = 0` or `g_beta = 0`. These are proper algebraic conditions, not an
independent action on every relation. The test suite checks this factorization
numerically and the enumeration finds explicit rational counterexamples to
independent invariance.

## Computational method

For each small prime, the program:

1. enumerates every rational point on the curve;
2. iterates over ordered pairs `(P,Q)`;
3. sets `R = -(P+Q)` when `R` is finite;
4. verifies `f3(x(P),x(Q),x(R)) = 0`;
5. tests diagonal and one-coordinate multiplication by `beta`; and
6. repeats the measurement on `y^2 = x^3 + 2*x + 7` as a field-matched
   control.

The relation count is an ordered-pair count, not a count modulo permutations,
point negation, or automorphism orbits.

## Baseline results

| `p` | `j=0` relations | diagonal rate | one-coordinate rate | control diagonal rate |
|---:|---:|---:|---:|---:|
| 19 | 110 | 1.0000 | 0.1818 | 0.0286 |
| 31 | 380 | 1.0000 | 0.1947 | 0.0427 |
| 37 | 1,406 | 1.0000 | 0.1038 | 0.0170 |
| 43 | 870 | 1.0000 | 0.0690 | 0.0107 |
| 61 | 3,540 | 1.0000 | 0.0339 | 0.0237 |

The diagonal `j = 0` result is exact and explained by the proposition. Every
observed one-coordinate survivor is explained by `x1 = 0` or the explicit
obstruction equation above. The rates are descriptive finite-field observations
only. These five fields are far too small and too few to support an asymptotic
claim.

## Interpretation

The obvious cube-root symmetry is real, but at the `f3` level it acts globally.
It does not permit each factor-base coordinate to be reduced independently.
Consequently, this experiment provides no evidence for an asymptotic reduction
in elliptic-curve discrete-logarithm complexity.

This result is useful as a guardrail: future algebraic experiments must measure
more than the already-known constant-size automorphism orbit.

## Limitations

- Only the third summation polynomial is studied.
- The fields are deliberately tiny and the curve groups need not have prime
  order.
- Relation existence is measured, not Gröbner-basis degree of regularity,
  relation-matrix rank, or end-to-end index-calculus cost.
- The control fixes `a = 2` and `b = 7`; broader matched curve families are
  needed.
- Exceptional points and repeated x-coordinates are included in aggregate
  counts.

## Next falsifiable experiment

Construct fourth and fifth summation-polynomial systems for matched `j = 0` and
generic curves, then compare after quotienting only the proven diagonal action:

- monomial count and multigraded support;
- degree reached during Gröbner-basis computation;
- peak basis size and elapsed operations; and
- rank and dependency structure of generated relation matrices.

The candidate hypothesis is that complex-multiplication symmetry lowers one of
these growth rates after proper quotienting. The null hypothesis is that it
provides only constant-factor savings. Evidence must be collected across
increasing primes and field-matched controls before extrapolating.

## Reproduction record

The implementation was developed proof-first. The initial tests failed because
the `j0lab` package and experiment entry point did not yet exist. A later test
also exposed that one arbitrarily selected relation was exceptional, which led
to full relation-set enumeration and the explicit obstruction identity.

Verification on 2026-10-10:

```text
python -m pytest
17 passed

python -m compileall -q src tests
completed without errors
```
