"""Measure aperture photometry for a set of star positions across a sequence of images."""

from pathlib import Path

from astropy.table import Table


def measure_aperture_photometry(
    image_paths: list[Path],
    positions: list[tuple[float, float]],
    aperture_radius: float,
    annulus_radii: tuple[float, float] | None = None,
) -> Table:
    """Return a table of flux measurements for each position in each image."""
    raise NotImplementedError
