"""Stack a sequence of images onto a common reference frame."""

from pathlib import Path
from dateutil import parser
from glob import glob
from collections.abc import Iterable 

from astropy.io import fits
import numpy as np

from eloy import detection
from eloy import alignment
from skimage.transform import warp


# detect stars in the reference image and return their coordinates
def detect_stars_coords(data):
    regions = detection.stars_detection(data)
    # stars coords and cutouts
    region_coords = np.array(
        [(r.centroid_weighted[1], r.centroid_weighted[0]) for r in regions]
    )

    return region_coords

# align the data with the detected stars in the reference image
def warp_data(data, ref_coords, ref_twirl):
    coords = detect_stars_coords(data)[0:15]
    X = alignment.rotation_matrix(coords, ref_coords, ref_twirl)
    warpped_data = warp(data.astype(float), X)
    return warpped_data


num_star_align = 15

def stack_images(
    image_paths: Iterable[Path],
    reference: Path
) -> astropy.io.fits.HDU:
    """Align image_paths to a reference image (the first, by default) and combine them into a single stacked image."""
    
    # detect stars in the reference image and return their coordinates
    ref_coords = detect_stars_coords(fits.getdata(reference))[0:num_star_align]
    ref_twirl = alignment.twirl_reference(ref_coords)

    # align and stack the images
    stack_image = np.zeros_like(fits.getdata(reference))
    for image in image_paths:
        aligned_image = warp_data(fits.getdata(image), ref_coords, ref_twirl)
        stack_image += aligned_image

    # this is maybe screwing up the wcs?
    # strange to be returning an HDU, not very api-ish
    # probably return the data and the header individually would be better
    header = fits.getheader(reference, extname='sci')
    header['EXTNAME'] = 'SCI'

    hdu = fits.PrimaryHDU(data=stack_image, header=header)

    return hdu