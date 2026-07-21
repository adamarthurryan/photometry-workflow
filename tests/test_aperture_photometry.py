import pytest

from photometry_workflow.aperture_photometry.api import measure_aperture_photometry
from photometry_workflow.aperture_photometry.cli import build_parser


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(
        [
            "a.fits",
            "b.fits",
            "c.fits",
            "-r",
            "ref.fits"
            "-o",
            "out.ecsv",
        ]
    )
    assert args.images == ["a.fits", "b.fits", "c.fits"]
    assert args.output == "out.ecsv"
    assert args.reference == "ref.fits"
