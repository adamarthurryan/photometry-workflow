"""Shared helpers for locating and loading image files used across tools."""

from pathlib import Path

FITS_EXTENSIONS = (".fits", ".fit", ".fts", ".fits.fz")


def resolve_image_paths(inputs: list[str]) -> list[Path]:
    """Expand a list of file/directory arguments into a sorted list of FITS file paths."""
    paths: list[Path] = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            paths.extend(
                sorted(f for f in p.iterdir() if f.suffix.lower() in FITS_EXTENSIONS)
            )
        else:
            paths.append(p)
    return sorted(set(paths))
