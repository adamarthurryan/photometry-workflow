import pytest
from astropy.table import Table

from photometry_workflow.differential_photometry.api import compute_differential_photometry
from photometry_workflow.differential_photometry.cli import build_parser


def test_compute_differential_photometry_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        compute_differential_photometry(Table(), [Table()])


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(
        [
            "--target",
            "target.ecsv",
            "--comparison",
            "comp1.ecsv",
            "--comparison",
            "comp2.ecsv",
            "-o",
            "out.ecsv",
        ]
    )
    assert args.target == "target.ecsv"
    assert args.comparisons == ["comp1.ecsv", "comp2.ecsv"]
    assert args.output == "out.ecsv"
