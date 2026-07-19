from pathlib import Path

import pytest

from photometry_workflow.comparison_stars.api import find_comparison_stars
from photometry_workflow.comparison_stars.cli import build_parser


def test_find_comparison_stars_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        find_comparison_stars(Path("a.fits"), target_position=(10.0, 20.0))


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(["a.fits", "--target", "10,20", "-o", "out.ecsv"])
    assert args.image == "a.fits"
    assert args.target == "10,20"
    assert args.output == "out.ecsv"
