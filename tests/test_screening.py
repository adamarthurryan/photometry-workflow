import pytest

from photometry_workflow.screening.api import screen_images
from photometry_workflow.screening.cli import build_parser


def test_screen_images_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        screen_images([])


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(["a.fits", "b.fits", "--min-stars", "5"])
    assert args.images == ["a.fits", "b.fits"]
    assert args.min_stars == 5
