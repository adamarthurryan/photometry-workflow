"""Command-line entry point for `photometry-screen`."""

import argparse
from pathlib import Path

from photometry_workflow.common.io import resolve_image_paths
from photometry_workflow.screening.api import screen_images


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photometry-screen",
        description="Screen and select images suitable for further processing.",
    )
    parser.add_argument("images", nargs="+", help="Image files or directories to screen")
    parser.add_argument("--min-stars", type=int, default=10)
    parser.add_argument("--max-fwhm", type=float, default=None)
    parser.add_argument("--max-background", type=float, default=None)
    parser.add_argument("-o", "--output", help="File to write the list of selected images to")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    image_paths = resolve_image_paths(args.images)

    selected = screen_images(
        image_paths,
        min_stars=args.min_stars,
        max_fwhm=args.max_fwhm,
        max_background=args.max_background,
    )

    lines = [str(p) for p in selected]
    if args.output:
        Path(args.output).write_text("\n".join(lines) + "\n")
    else:
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()
