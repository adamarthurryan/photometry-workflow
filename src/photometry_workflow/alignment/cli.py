"""Command-line entry point for `pw-align`."""

import argparse
from pathlib import Path

from photometry_workflow.alignment.api import align_images
from photometry_workflow.common.io import resolve_image_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pw-align",
        description="Align a sequence of images onto a common reference frame.",
    )
    parser.add_argument("images", nargs="+", help="Image files or directories to align")
    parser.add_argument("-o", "--output-dir", required=True, help="Directory to write aligned images to")
    parser.add_argument("-r", "--reference", help="Path to the reference image (default: first image)")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    image_paths = resolve_image_paths(args.images)
    reference = Path(args.reference) if args.reference else None

    aligned = align_images(image_paths, output_dir=Path(args.output_dir), reference=reference)

    for path in aligned:
        print(path)


if __name__ == "__main__":
    main()
