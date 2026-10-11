# secp256k1 j=0 algebra lab

This repository studies whether the extra algebraic structure of `j = 0`
elliptic curves can simplify relation-based discrete-logarithm methods. It uses
small, generated finite fields so every result is reproducible without touching
real keys or live cryptocurrency systems.

The first experiment checks how the order-three map

```text
phi(x, y) = (beta*x, y), where beta^3 = 1 and beta != 1,
```

acts on Semaev's third summation polynomial for curves
`y^2 = x^3 + b`. The diagonal action preserves the polynomial's zero set. The
same action on one coordinate alone has an explicit nonzero obstruction and
does not preserve all relations, so it does not immediately give an independent
factor-base quotient.

This is a reproducible baseline and negative result, not a claim to have broken
secp256k1. See [the research note](docs/research-note.md) for the proposition,
evidence, limitations, and next hypothesis.

## Run the experiment

Python 3.11 or newer is required.

```powershell
python -m pip install -e '.[dev]'
python -m pytest
j0lab --pretty
```

Without installing the package:

```powershell
$env:PYTHONPATH = 'src'
python -m j0lab.cli --pretty
```

The command emits versioned JSON containing paired results for each `j = 0`
curve and a matched nonzero-`a` control over the same field.

## Research principles

- State a falsifiable hypothesis before adding an experiment.
- Compare structured curves with field-matched controls.
- Report negative and null results.
- Separate finite-field observations from asymptotic claims.
- Use only generated toy instances with no monetary value.
- Privately coordinate review before releasing any result that plausibly lowers
  the security of production-size curves.

## References

- SEC 2, *Recommended Elliptic Curve Domain Parameters*, version 2.0.
  https://www.secg.org/sec2-v2.pdf
- Amadori, Pintore, and Sala, *On the discrete logarithm problem for
  prime-field elliptic curves*. https://eprint.iacr.org/2017/609
- Shoup, *Lower Bounds for Discrete Logarithms and Related Problems*.
  https://doi.org/10.1007/3-540-69053-0_18

## License

Code and documentation are available under the MIT License.
