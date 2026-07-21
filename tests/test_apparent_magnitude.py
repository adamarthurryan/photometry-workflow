import pytest
from astropy.table import Table

from photometry_workflow.apparent_magnitude.api import estimate_apparent_magnitude
from photometry_workflow.apparent_magnitude.cli import build_parser


def test_estimate_apparent_magnitude_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        estimate_apparent_magnitude(Table(), Table(), Table())


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(
        [
            "--sources",
            "sources.ecsv",
            "--images",
            "images.ecsv",
            "--flux",
            "flux.ecsv",
            "-o",
            "magnitudes.ecsv",
        ]
    )
    assert args.sources == "sources.ecsv"
    assert args.images == "images.ecsv"
    assert args.flux == "flux.ecsv"
    assert args.output == "magnitudes.ecsv"
