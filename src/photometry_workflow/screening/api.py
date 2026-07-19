"""Screen and select images suitable for further processing."""

from pathlib import Path


def screen_images(
    image_paths: list[Path],
    min_stars: int = 10,
    max_fwhm: float | None = None,
    max_background: float | None = None,
) -> list[Path]:
    """Return the subset of image_paths that pass quality screening criteria."""
    raise NotImplementedError
