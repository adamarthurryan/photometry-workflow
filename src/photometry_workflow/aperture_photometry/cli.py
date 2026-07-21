"""Command-line entry point for `pw-aperture`."""

import argparse
from pathlib import Path

from photometry_workflow.aperture_photometry.api import measure_aperture_photometry
from photometry_workflow.common.io import resolve_image_paths

from tqdm import tqdm 

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pw-aperture",
        description="Measure aperture photometry for all sources across a sequence of images.",
    )
    parser.add_argument("images", nargs="+", help="Image files or directories to measure")
    parser.add_argument("-o", "--output", required=True, help="Folder to write the flux and sources tables to")
    parser.add_argument("-f", "--format", default="hdf5", choices=["hdf5", "ecsv", "fits"], help="File extension for the flux and photometry tables")
    parser.add_argument("-r", "--reference", help="Reference image to extract sources from (defaults to the first image)")
    return parser


def _parse_pair(text: str) -> tuple[float, float]:
    a, b = text.split(",")
    return float(a), float(b)


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    image_paths = resolve_image_paths(args.images)
    reference_path = Path(args.reference) if args.reference else image_paths[0]
    flux_path = Path(args.output, "flux."+args.format)
    sources_path = Path(args.output, "sources."+args.format)

    print(flux_path, sources_path)

    flux_table, sources_table = measure_aperture_photometry(
        tqdm(image_paths),
        reference_path=reference_path
    )

    flux_table.write(flux_path, overwrite=True)
    sources_table.write(sources_path, overwrite=True)


if __name__ == "__main__":
    main()
