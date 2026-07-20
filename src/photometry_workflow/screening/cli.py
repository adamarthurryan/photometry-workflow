"""Command-line entry point for `pw-screen`."""

import argparse
from pathlib import Path

from photometry_workflow.common.io import resolve_image_paths
from photometry_workflow.screening.api import screen_images

from tqdm import tqdm

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pw-screen",
        description="Screen and select images suitable for further processing.",
    )
    parser.add_argument("images", nargs="+", help="Image files or directories to screen")
    parser.add_argument("-o", "--output", help="File to write the list of selected images to")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    image_paths = resolve_image_paths(args.images)

    selected = screen_images(
        tqdm(image_paths)
    )

    lines = [str(p) for p in selected]
    if args.output:
        Path(args.output).write_text("\n".join(lines) + "\n")
    else:
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()
