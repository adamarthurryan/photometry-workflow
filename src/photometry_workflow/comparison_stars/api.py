"""Identify suitable comparison stars for differential photometry of a target star."""

from pathlib import Path

from astropy.table import Table


def find_comparison_stars(
    image_path: Path,
    target_position: tuple[float, float],
    max_candidates: int = 10,
    max_magnitude_difference: float | None = None,
) -> Table:
    """Return a table of candidate comparison stars near target_position, ranked by suitability."""
    raise NotImplementedError
