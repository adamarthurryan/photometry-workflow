"""Measure aperture photometry for a set of star positions across a sequence of images."""

from pathlib import Path
from dateutil import parser
from collections.abc import Iterable 

import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy.time import Time
from astropy.wcs import WCS

from skimage.transform import AffineTransform, warp

from eloy import alignment, viz
from eloy import psf, detection, utils
from eloy import centroid, photometry

from photometry_workflow.common.cross_match import cross_match_gaia
from photometry_workflow.common.error import ccd_flux_error, annulus_sigma_clip_std


# get observation time from FITS header (SCI extension)
def observation_time(file):

    sci_header = fits.getheader(file, extname='sci')
    date_str = sci_header["DATE-OBS"]
    return parser.parse(date_str)


trim = 10
n_stars_align = 12

def calibration_sequence(file):
    # getting data
    data = fits.getdata(file)

    # trimming
    #calibrated_data = data[trim:-trim, trim:-trim]
    calibrated_data = data

    # detection
    regions = detection.stars_detection(calibrated_data)
    # stars coords and cutouts
    region_coords = np.array([(r.centroid[1], r.centroid[0]) for r in regions])
    cutouts = utils.cutout(calibrated_data, region_coords, (50, 50))

    # epsf modeling
    cutouts_normalized = cutouts / np.nanmax(cutouts, (1, 2))[:, None, None]
    epsf = np.nanmedian(cutouts_normalized, 0)
    psf_params = psf.fit_gaussian(epsf)
    fwhm = psf.gaussian_sigma_to_fwhm * np.mean(
        [psf_params["sigma_x"], psf_params["sigma_y"]]
    )

    return calibrated_data, region_coords, fwhm

n_stars = 100
relative_apertures_radii = np.linspace(0.1, 5, 40)


def do_flux_measurement(image_path, ref_coords, ref_twirl) :
    calibrated_data, coords, fwhm = calibration_sequence(image_path)

    # alignment
    R = alignment.rotation_matrix(coords[0:n_stars_align], ref_coords, ref_twirl)
    transform = AffineTransform(R)
    aligned_coords = transform(ref_coords)[0:n_stars]
    dx, dy = np.median(ref_coords[0:n_stars] - aligned_coords, 0)

    # centroiding
    centroid_coords = centroid.photutils_centroid(calibrated_data, aligned_coords)
    
    # aperture photometry
    apertures_radii = relative_apertures_radii * fwhm
    flux = photometry.aperture_photometry(
        calibrated_data, centroid_coords, apertures_radii
    )

    # annulus background correction
    annulus_radii = np.max(apertures_radii), 8 * fwhm
    aperture_area = np.pi * apertures_radii**2
    bkg = photometry.annulus_sigma_clip_median(
        calibrated_data, centroid_coords, *annulus_radii
    )
    bkg_flux = bkg[:, None] * aperture_area[None, :]
    src_flux = flux-bkg_flux

    # get info from header
    sci_header = fits.getheader(image_path, extname='sci')
    date_str = sci_header["DATE-OBS"]
    jd = Time(parser.parse(date_str)).jd
    filter = sci_header["FILTER"] 
    dark_current = sci_header["DARKCURR"]
    read_noise = sci_header["RDNOISE"]
    exposure_time = sci_header["EXPTIME"]
    gain = sci_header["GAIN"]

    n_sky = np.pi*annulus_radii[1]**2 - np.pi*annulus_radii[0]**2
    sigma_sky = annulus_sigma_clip_std(calibrated_data, centroid_coords, *annulus_radii)

    # calculate flux error
    src_flux_error = ccd_flux_error(src_flux, aperture_area, sigma_sky, n_sky, gain, read_noise)

    # format and output
    image_stats = {"time":jd, "dx":dx, "dy":dy, "fwhm":fwhm, 
                   "exposure_time": exposure_time, "filter":filter, "dark_current": dark_current, "read_noise": read_noise, "gain": gain,
                   "apertures_radii": apertures_radii, "annulus_radii": annulus_radii
                   }

    flux_data = {"bkg_flux":bkg_flux,  "src_flux":src_flux, "src_flux_error":src_flux_error}

    return image_stats, flux_data
  

def measure_aperture_photometry(
    image_paths: Iterable[Path],
    reference_path: Path
) -> tuple[Table, Table, Table]:
    """Measure aperture photometry for each source in the reference image, across a sequence of images.

    Returns three tables, normalized and linked by id columns:
     - source_table: one row per reference-image source, keyed by `source_id`,
       cross-matched to Gaia photometry (`gaia_matched` indicates whether the match
       cleared the accuracy threshold).
     - image_table: one row per input image, keyed by `image_id`, with per-image
       measurements (time, alignment offset, fwhm, filter, readout noise, etc).
     - flux_table: one row per (image, source) pair, referencing `image_id` and
       `source_id`, with the flux and background measurements.
    """

    # get the sources from the reference image
    ref_data, ref_coords, ref_fwhm = calibration_sequence(reference_path)

    # truncate up front so every downstream table (sources, fluxes) covers the same
    # set of sources, in the same order
    ref_coords = ref_coords[0:n_stars]
    ref_twirl = alignment.twirl_reference(ref_coords[0:n_stars_align])
    ref_header = fits.getheader(reference_path, extname="sci")
    wcs = WCS(ref_header)

    # create a table cross matching sources to Gaia photometry
    source_table = cross_match_gaia(ref_coords, wcs)
    source_table.add_column(np.arange(len(source_table)), name="source_id", index=0)

    # do photometry on each image, building the per-image and per-(image, source) tables
    image_rows = []
    flux_rows = []
    for image_id, image_path in enumerate(image_paths):
        image_stats, flux_data = do_flux_measurement(image_path, ref_coords, ref_twirl)

        image_stats["image_id"]=image_id
        image_rows.append(image_stats)

        for source_id in range(len(source_table)):
            flux_rows.append({
                "image_id": image_id,
                "source_id": source_id,
                "bkg_flux": flux_data["bkg_flux"][source_id],
                "src_flux": flux_data["src_flux"][source_id],
                "src_flux_error": flux_data["src_flux_error"][source_id]
            })

    image_table = Table(image_rows)
    flux_table = Table(flux_rows)

    return source_table, image_table, flux_table
