import json

import pytest

from j0lab.cli import main
from j0lab.experiment import analyze_curve


@pytest.mark.parametrize("prime", [19, 31, 37, 43, 61])
def test_j0_diagonal_action_preserves_every_enumerated_relation(prime: int) -> None:
    result = analyze_curve(p=prime, a=0, b=7)

    assert result.relation_count > 0
    assert result.diagonal_preserved == result.relation_count
    assert result.single_coordinate_preserved < result.relation_count
    assert result.single_preserved_unexplained == 0


def test_matched_control_does_not_have_the_j0_diagonal_action() -> None:
    result = analyze_curve(p=31, a=2, b=7)

    assert result.relation_count > 0
    assert result.diagonal_preserved < result.relation_count


def test_cli_emits_machine_readable_paired_results(capsys) -> None:
    exit_code = main(["--primes", "31"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["schema_version"] == 1
    assert payload["experiments"][0]["j0"]["p"] == 31
    assert payload["experiments"][0]["control"]["a"] == 2
