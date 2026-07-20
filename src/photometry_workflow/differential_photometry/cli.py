"""Command-line entry point for `pw-diffphot`."""

import argparse

from astropy.table import Table

from photometry_workflow.differential_photometry.api import compute_differential_photometry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pw-diffphot",
        description="Compute differential photometry of a target star relative to comparison stars.",
    )
    parser.add_argument("--target", required=True, help="Path to the target star's photometry table")
    parser.add_argument(
        "--comparison",
        action="append",
        required=True,
        dest="comparisons",
        metavar="PATH",
        help="Path to a comparison star's photometry table. May be repeated.",
    )
    parser.add_argument("-o", "--output", required=True, help="Path to write the light curve table to")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    target_photometry = Table.read(args.target)
    comparison_photometry = [Table.read(p) for p in args.comparisons]

    light_curve = compute_differential_photometry(target_photometry, comparison_photometry)
    light_curve.write(args.output, overwrite=True)


if __name__ == "__main__":
    main()
