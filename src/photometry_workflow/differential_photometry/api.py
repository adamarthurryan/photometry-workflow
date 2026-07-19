"""Compute differential photometry of a target star relative to comparison stars."""

from astropy.table import Table


def compute_differential_photometry(
    target_photometry: Table,
    comparison_photometry: list[Table],
) -> Table:
    """Return a light curve table of the target's magnitude relative to the comparison ensemble."""
    raise NotImplementedError
