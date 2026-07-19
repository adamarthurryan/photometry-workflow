"""Align a sequence of images onto a common reference frame."""

from pathlib import Path


def align_images(
    image_paths: list[Path],
    output_dir: Path,
    reference: Path | None = None,
) -> list[Path]:
    """Align image_paths to a reference image (the first, by default) and write results to output_dir."""
    raise NotImplementedError
