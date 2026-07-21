"""Command-line entry point for `pw-stack`."""

import argparse
from pathlib import Path

from tqdm import tqdm

from astropy.io import fits

from photometry_workflow.stack.api import stack_images
from photometry_workflow.common.io import resolve_image_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pw-stack",
        description="Stack a sequence of images onto a common reference frame.",
    )
    parser.add_argument("images", nargs="+", help="Image files or directories to stack")
    parser.add_argument("-r", "--reference", help="Reference image to align to (defaults to the first image)")
    parser.add_argument("-o", "--output", required=True, help="File for the stacked image")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    image_paths = resolve_image_paths(args.images)
    reference = Path(args.reference) if args.reference else image_paths[0]

    stacked_hdu = stack_images(tqdm(image_paths), reference=reference)

    output = Path(args.output)
    stacked_hdu.writeto(output, overwrite=True)


if __name__ == "__main__":
    main()
