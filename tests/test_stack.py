import pytest

from photometry_workflow.stack.api import stack_images
from photometry_workflow.stack.cli import build_parser


def test_stack_images_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        stack_images([])


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(["a.fits", "b.fits", "-o", "out.fits", "-r", "a.fits"])
    assert args.images == ["a.fits", "b.fits"]
    assert args.output == "out.fits"
    assert args.reference == "a.fits"
