# cross match target stars from GAIA DR3 Synthetic Photometry Catalogue

from astroquery.gaia import Gaia
from astropy.wcs.utils import pixel_to_skycoord
from astropy.coordinates import match_coordinates_sky, SkyCoord
from astropy.wcs.utils import pixel_to_skycoord
from astropy.table import hstack, QTable, Table
import astropy.units as u 



def cross_match_gaia(centroid_coords, wcs, limit_magnitude=16, min_accuracy=2*u.arcsec) -> Table:

    # bound the query by the polygon formed by the image's four corners, walked around
    # the perimeter, rather than a box derived from the center and width/height
    (img_width, img_height) = wcs.pixel_shape
    corner_x = [0, img_width, img_width, 0]
    corner_y = [0, 0, img_height, img_height]
    corner_coords = wcs.pixel_to_world(corner_x, corner_y)

    limit_magnitude = 16

    query = create_gaia_query(corner_coords.ra.deg, corner_coords.dec.deg, limit_magnitude)
    job = Gaia.launch_job(query)
    gaia_table: Table = job.get_results()

    # TODO: error handling for failed job

    centroid_skycoords = pixel_to_skycoord(*centroid_coords.T, wcs)

    #extract coordinates of catalog stars
    gaia_skycoords = SkyCoord(gaia_table["ra"], gaia_table["dec"], frame="icrs")

    # match the gaia coords to the centroid coords
    gaia_match = match_coordinates_sky(centroid_skycoords, gaia_skycoords)
    indices = gaia_match[0]
    gaia_matched = gaia_match[1] < min_accuracy

    # create a table, one row per input coordinate (order and length preserved)
    centroid_table = QTable([centroid_coords.T[0], centroid_coords.T[1],centroid_skycoords.ra, centroid_skycoords.dec, gaia_match[1], gaia_matched],
                            names=["centroid_x", "centroid_y", "centroid_ra","centroid_dec", "gaia_match_err", "gaia_matched"])

    # rename Gaia's own source_id so it doesn't collide with a source_id column a caller may add
    gaia_rows = gaia_table[indices].copy()
    gaia_rows.rename_column("source_id", "gaia_source_id")

    # rows that didn't clear min_accuracy only found a *nearest* candidate, not a real
    # match, so mask out the Gaia-derived columns for those rows rather than keep them
    gaia_rows = Table(gaia_rows, masked=True)
    for colname in gaia_rows.colnames:
        gaia_rows[colname].mask = ~gaia_matched

    catalog_table = hstack([centroid_table, gaia_rows])

    return catalog_table

def create_gaia_query(corner_ra, corner_dec, limit_mag):
    where_limit_mag = f"src.phot_g_mean_mag < {limit_mag}"

    polygon_points = ", ".join(f"{ra}, {dec}" for ra, dec in zip(corner_ra, corner_dec))
    where_polygon_search = f"""1 = CONTAINS(
                POINT(src.ra, src.dec),
                POLYGON({polygon_points})
            )"""

    query = f"""
    SELECT src.ra, src.dec, gspc.*
        FROM gaiadr3.synthetic_photometry_gspc AS gspc
        JOIN gaiadr3.gaia_source AS src
            ON gspc.source_id = src.source_id

        WHERE {where_limit_mag}
            AND {where_polygon_search}
        ;
    """

    return query
