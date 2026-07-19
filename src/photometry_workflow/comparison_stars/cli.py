"""Command-line entry point for `photometry-compstars`."""

import argparse
from pathlib import Path

from photometry_workflow.comparison_stars.api import find_comparison_stars


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photometry-compstars",
        description="Identify suitable comparison stars for differential photometry of a target star.",
    )
    parser.add_argument("image", help="Reference image to search for comparison stars")
    parser.add_argument("--target", required=True, metavar="X,Y", help="Pixel position of the target star, as 'x,y'")
    parser.add_argument("--max-candidates", type=int, default=10)
    parser.add_argument("--max-magnitude-difference", type=float, default=None)
    parser.add_argument("-o", "--output", required=True, help="Path to write the candidate table to")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    x, y = (float(v) for v in args.target.split(","))

    table = find_comparison_stars(
        Path(args.image),
        target_position=(x, y),
        max_candidates=args.max_candidates,
        max_magnitude_difference=args.max_magnitude_difference,
    )
    table.write(args.output, overwrite=True)


if __name__ == "__main__":
    main()
