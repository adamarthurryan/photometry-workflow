"""Estimate calibrated apparent magnitude for each source, using Gaia-matched sources
as photometric calibrators."""

from astropy.table import Table


def estimate_apparent_magnitude(
    source_table: Table,
    image_table: Table,
    flux_table: Table,
    magnitude_column: str = "phot_g_mean_mag",
) -> Table:
    """Return a table of estimated apparent magnitude for each (image, source) pair.

    Sources with a Gaia match (`gaia_matched` in source_table) provide a per-image
    zero-point calibration, derived from `magnitude_column`, that is applied to every
    source's instrumental flux in that image.
    """
    raise NotImplementedError
