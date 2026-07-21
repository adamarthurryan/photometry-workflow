# cross match target stars from GAIA DR3 Synthetic Photometry Catalogue

from astroquery.gaia import Gaia
from astropy.wcs.utils import pixel_to_skycoord
from astropy.coordinates import match_coordinates_sky, SkyCoord
from astropy.wcs.utils import pixel_to_skycoord
from astropy.table import hstack, QTable, Table
import astropy.units as u 



def cross_match_gaia(centroid_coords, wcs, limit_magnitude=16, min_accuracy=2*u.arcsec) -> Table:

    # !!! TODO: this is not the correct bounds calculation
    # should use a polygon or a box around the image, not just the center and the width/height

    # calculate the rough bounds of the image
    (img_width, img_height) = wcs.pixel_shape
    img_center_coord = wcs.pixel_to_world(img_width/2, img_height/2)
    img_top_left = wcs.pixel_to_world(0, 0)
    img_coord_width = img_top_left.separation(wcs.pixel_to_world(img_width, 0))
    img_coord_height = img_top_left.separation(wcs.pixel_to_world(0, img_height))

    limit_magnitude = 16
    
    query = create_gaia_query(img_center_coord.ra.deg, img_center_coord.dec.deg, img_coord_width.deg, img_coord_height.deg, limit_magnitude)
    job = Gaia.launch_job(query)
    gaia_table: Table = job.get_results()

    # TODO: error handling for failed job

    centroid_skycoords = pixel_to_skycoord(*centroid_coords.T, wcs)

    #extract coordinates of catalog stars
    gaia_skycoords = SkyCoord(gaia_table["ra"], gaia_table["dec"], frame="icrs")

    # match the gaia coords to the centroid coords
    gaia_match = match_coordinates_sky(centroid_skycoords, gaia_skycoords)
    print (gaia_match)

    indices = gaia_match[0]


    # create a table  
    centroid_table = QTable([centroid_coords.T[0], centroid_coords.T[1],centroid_skycoords.ra, centroid_skycoords.dec, gaia_match[1]], 
                            names=["centroid_x", "centroid_y", "centroid_ra","centroid_dec", "gaia_match_err"])

    print (centroid_table[centroid_table["gaia_match_err"]<min_accuracy])



    catalog_table = hstack([centroid_table, gaia_table[indices]])
    catalog_table_masked = catalog_table[(catalog_table["gaia_match_err"]<min_accuracy) ]

    return catalog_table_masked

def create_gaia_query(center_ra, center_dec, width_ra, width_dec, limit_mag):
    where_limit_mag = f"src.phot_g_mean_mag < {limit_mag}"

    where_box_search = f"""1 = CONTAINS(
                POINT(src.ra, src.dec), 
                BOX({center_ra}, {center_dec}, {width_ra}, {width_dec})
            )"""

    query = f"""
    SELECT src.ra, src.dec, gspc.*
        FROM gaiadr3.synthetic_photometry_gspc AS gspc
        JOIN gaiadr3.gaia_source AS src 
            ON gspc.source_id = src.source_id
        
        WHERE {where_limit_mag} 
            AND {where_box_search}
        ;
    """

    return query
