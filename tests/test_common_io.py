from pathlib import Path

from photometry_workflow.common.io import resolve_image_paths


def test_resolve_image_paths_expands_directory(tmp_path: Path) -> None:
    fits_file = tmp_path / "a.fits"
    fits_file.touch()
    (tmp_path / "notes.txt").touch()

    assert resolve_image_paths([str(tmp_path)]) == [fits_file]


def test_resolve_image_paths_passes_through_files(tmp_path: Path) -> None:
    fits_file = tmp_path / "a.fits"
    fits_file.touch()

    assert resolve_image_paths([str(fits_file)]) == [fits_file]
