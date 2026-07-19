from pathlib import Path

import pytest

from photometry_workflow.alignment.api import align_images
from photometry_workflow.alignment.cli import build_parser


def test_align_images_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        align_images([], output_dir=Path("out"))


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(["a.fits", "b.fits", "-o", "out/", "-r", "a.fits"])
    assert args.images == ["a.fits", "b.fits"]
    assert args.output_dir == "out/"
    assert args.reference == "a.fits"
