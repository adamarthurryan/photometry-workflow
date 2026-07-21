from pathlib import Path

import numpy as np
import pytest
from astropy.table import Table

from photometry_workflow.aperture_photometry import api
from photometry_workflow.aperture_photometry.api import measure_aperture_photometry
from photometry_workflow.aperture_photometry.cli import build_parser


def test_cli_parses_required_arguments() -> None:
    args = build_parser().parse_args(
        [
            "a.fits",
            "b.fits",
            "c.fits",
            "-r",
            "ref.fits",
            "-o",
            "outfolder",
        ]
    )
    assert args.images == ["a.fits", "b.fits", "c.fits"]
    assert args.output == "outfolder"
    assert args.reference == "ref.fits"


def test_measure_aperture_photometry_links_sources_images_and_flux(monkeypatch) -> None:
    n_sources = 3
    ref_coords = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])

    monkeypatch.setattr(api, "calibration_sequence", lambda path: (None, ref_coords, 2.0))
    monkeypatch.setattr(api.alignment, "twirl_reference", lambda coords: "ref_twirl")
    monkeypatch.setattr(api.fits, "getheader", lambda path, extname=None: {})
    monkeypatch.setattr(api, "WCS", lambda header: object())
    monkeypatch.setattr(
        api, "cross_match_gaia",
        lambda coords, wcs: Table({"centroid_x": coords[:, 0], "centroid_y": coords[:, 1]}),
    )

    def fake_do_flux_measurement(image_path, coords, twirl):
        return {
            "time": image_paths.index(image_path),
            "dx": 0.0,
            "dy": 0.0,
            "fwhm": 2.0,
            "bkg": np.arange(n_sources * 2).reshape(n_sources, 2),
            "fluxes": np.arange(n_sources * 2).reshape(n_sources, 2) * 10,
        }

    monkeypatch.setattr(api, "do_flux_measurement", fake_do_flux_measurement)

    image_paths = [Path("a.fits"), Path("b.fits")]

    source_table, image_table, flux_table = measure_aperture_photometry(
        image_paths, reference_path=Path("ref.fits")
    )

    assert list(source_table["source_id"]) == [0, 1, 2]
    assert list(image_table["image_id"]) == [0, 1]

    # every (image_id, source_id) pair in flux_table must resolve against the other two tables
    assert len(flux_table) == len(image_paths) * n_sources
    assert set(flux_table["image_id"]) <= set(image_table["image_id"])
    assert set(flux_table["source_id"]) <= set(source_table["source_id"])
