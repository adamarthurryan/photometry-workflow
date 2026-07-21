from pathlib import Path

import pytest

from photometry_workflow.sources.api import find_sources
from photometry_workflow.sources.cli import build_parser


def test_find_sources_not_yet_implemented() -> None:
    with pytest.raises(NotImplementedError):
        find_sources(Path("ref.fits"))


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(["ref.fits", "-o", "sources.csv"])
    assert args.image == "ref.fits"
    assert args.output == "sources.csv"
