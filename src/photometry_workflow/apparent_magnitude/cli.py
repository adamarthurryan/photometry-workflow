"""Command-line entry point for `pw-magnitude`."""

import argparse

from astropy.table import Table

from photometry_workflow.apparent_magnitude.api import estimate_apparent_magnitude


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pw-magnitude",
        description="Estimate calibrated apparent magnitude for each source, using Gaia-matched sources as photometric calibrators.",
    )
    parser.add_argument("--sources", required=True, help="Path to the sources table from pw-aperture")
    parser.add_argument("--images", required=True, help="Path to the images table from pw-aperture")
    parser.add_argument("--flux", required=True, help="Path to the flux table from pw-aperture")
    parser.add_argument(
        "-m", "--magnitude-column", default="phot_g_mean_mag",
        help="Gaia magnitude column to calibrate against (default: phot_g_mean_mag)",
    )
    parser.add_argument("-o", "--output", required=True, help="Path to write the magnitude table to")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    source_table = Table.read(args.sources)
    image_table = Table.read(args.images)
    flux_table = Table.read(args.flux)

    magnitude_table = estimate_apparent_magnitude(
        source_table, image_table, flux_table, magnitude_column=args.magnitude_column
    )
    magnitude_table.write(args.output, overwrite=True)


if __name__ == "__main__":
    main()
