"""Command-line entry point for `photometry-aperture`."""

import argparse
from pathlib import Path

from photometry_workflow.aperture_photometry.api import measure_aperture_photometry
from photometry_workflow.common.io import resolve_image_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photometry-aperture",
        description="Measure aperture photometry for a set of star positions across a sequence of images.",
    )
    parser.add_argument("images", nargs="+", help="Image files or directories to measure")
    parser.add_argument(
        "--position",
        action="append",
        required=True,
        dest="positions",
        metavar="X,Y",
        help="Pixel position of a star, given as 'x,y'. May be repeated.",
    )
    parser.add_argument("--aperture-radius", type=float, required=True)
    parser.add_argument(
        "--annulus-radii",
        metavar="INNER,OUTER",
        help="Background annulus radii, given as 'inner,outer'",
    )
    parser.add_argument("-o", "--output", required=True, help="Path to write the photometry table to")
    return parser


def _parse_pair(text: str) -> tuple[float, float]:
    a, b = text.split(",")
    return float(a), float(b)


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    image_paths = resolve_image_paths(args.images)
    positions = [_parse_pair(p) for p in args.positions]
    annulus_radii = _parse_pair(args.annulus_radii) if args.annulus_radii else None

    table = measure_aperture_photometry(
        image_paths,
        positions=positions,
        aperture_radius=args.aperture_radius,
        annulus_radii=annulus_radii,
    )
    table.write(args.output, overwrite=True)


if __name__ == "__main__":
    main()
