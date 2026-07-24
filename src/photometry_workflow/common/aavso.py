"""Fetch photometric comparison-star sequences from the AAVSO Variable Star Plotter (VSP)."""

import numpy as np
import requests
from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as u

VSP_CHART_URL = "https://app.aavso.org/vsp/api/chart/"


def fetch_vsp_sequence(
    star_name: str,
    fov: float = 60,
    maglimit: float = 16,
    bands: tuple[str, ...] = ("B", "V", "Rc", "Ic"),
) -> tuple[SkyCoord, Table]:
    """Fetch a comparison-star sequence for a named variable star from AAVSO VSP.

    Returns:
     - target_coord: sky coordinate of `star_name`, as resolved by AAVSO
     - sequence_table: one row per comparison star, with `auid`, `label`, sky
       coordinates, and `<band>_mag`/`<band>_error` columns for each of `bands`
       (masked where a star has no measurement in that band)
    """
    response = requests.get(
        VSP_CHART_URL,
        params={"format": "json", "star": star_name, "fov": fov, "maglimit": maglimit},
        timeout=30,
    )
    response.raise_for_status()
    chart = response.json()

    target_coord = SkyCoord(chart["ra"], chart["dec"], unit=(u.hourangle, u.deg))

    rows = []
    for star in chart["photometry"]:
        band_mags = {b["band"]: (b["mag"], b["error"]) for b in star["bands"]}
        row = {"auid": star["auid"], "label": star["label"], "ra": star["ra"], "dec": star["dec"]}
        for band in bands:
            mag, error = band_mags.get(band, (np.nan, np.nan))
            row[f"{band}_mag"] = mag
            row[f"{band}_error"] = error
        rows.append(row)

    sequence_table = Table(rows)
    sequence_coords = SkyCoord(sequence_table["ra"], sequence_table["dec"], unit=(u.hourangle, u.deg))
    sequence_table["ra"] = sequence_coords.ra
    sequence_table["dec"] = sequence_coords.dec

    return target_coord, sequence_table
