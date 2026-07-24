"""Screen and select images suitable for further processing."""

from pathlib import Path
import pandas as pd
import numpy as np
from astropy.io import fits

from astropy.stats import SigmaClip, sigma_clipped_stats
from photutils.background import Background2D, MedianBackground

from photutils.psf import fit_fwhm
from photutils.detection import DAOStarFinder
from astropy.stats import mad_std

# !!! TODO: convert this to the faster Eloy workflow as in aperture_photometry and stack

def calculate_image_statistics(image_path: Path) -> dict:
    """Calculate statistics for a single image.

    Parameters:
    - image_path (Path): Path to the image file.

    Returns:
    - dict: Dictionary containing calculated statistics.
    """

    data = fits.getdata(image_path)

    # get sigma-clipped image stats
    mean, median, std = sigma_clipped_stats(data, sigma=3.0)

    # create a low-res background map
    sigma_clip = SigmaClip(sigma=3.0)
    bkg_estimator = MedianBackground()
    bkg = Background2D(data, (100, 100), filter_size=(3, 3), 
                    sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)

    # background-subtract the data for clean profiling
    data_sub = data - bkg.background

    # find sources
    guess_fwhm=4.0
    daofind = DAOStarFinder(fwhm=guess_fwhm, threshold=5.0 * std, peak_max=50000)
    sources = daofind(data_sub)

    # filter sources by sharpness (DAOPhot defaults for stars are typically between 0.2 and 1.0)
    good_shape = (sources['sharpness'] > 0.2) & (sources['sharpness'] < 1.0)
    valid_stars = sources[good_shape]

    # filter sources by flux (get the top 10% brightest of the valid stars)
    flux_limit = np.percentile(valid_stars['flux'], 90)
    bright_stars = valid_stars[valid_stars['flux'] >= flux_limit]

    # pull out the centroids
    centroid_xy = np.array([bright_stars['x_centroid'], bright_stars['y_centroid']]).T
    
    fwhms = fit_fwhm(data_sub, xypos=centroid_xy, fwhm=guess_fwhm, fit_shape=7)
    fwhm_med = np.nanmedian(fwhms)
    fwhm_mad = mad_std(fwhms)

    # todo: eccentricity / ellipticity calculation

    return {
        "image_path": image_path,
        "num_stars": len(sources),
        "fwhm": fwhm_med
    }

def screen_images(
    image_paths: list[Path], verbose=False
) -> list[Path]:
    """Return the subset of image_paths that pass quality screening criteria."""

    # calculate statistics for each image
    stats_list_of_dict = [calculate_image_statistics(img) for img in image_paths]

    stats = pd.DataFrame(stats_list_of_dict)

    if verbose:
        print("Stats")
        print(stats)

    thresholds = {
        "fwhm": stats["fwhm"].median() * 1.5,
        "num_stars": stats["num_stars"].median() * 0.5
    }

    if verbose:
        print(f"Screening thresholds: {thresholds}")


    # return filtered images
    fwhm_filter = stats["fwhm"] <= thresholds["fwhm"]
    num_stars_filter = stats["num_stars"] >= thresholds["num_stars"]

    return stats[fwhm_filter & num_stars_filter]["image_path"].tolist()
