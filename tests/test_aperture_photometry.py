import pytest

from photometry_workflow.aperture_photometry.api import measure_aperture_photometry
from photometry_workflow.aperture_photometry.cli import build_parser


def test_measure_aperture_photometry_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        measure_aperture_photometry([], positions=[(1.0, 2.0)], aperture_radius=5.0)


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(
        [
            "a.fits",
            "--position",
            "10,20",
            "--position",
            "30,40",
            "--aperture-radius",
            "5",
            "-o",
            "out.ecsv",
        ]
    )
    assert args.images == ["a.fits"]
    assert args.positions == ["10,20", "30,40"]
    assert args.aperture_radius == 5.0
    assert args.output == "out.ecsv"
