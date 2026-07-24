from photutils.aperture import CircularAperture, CircularAnnulus
from astropy.stats import sigma_clipped_stats
import numpy as np

def ccd_flux_error(flux_net, area_ap, sigma_sky, n_sky, gain=1, readout_noise=0.0):
    """
    Calculates flux error using the CCD equation for Gain = 1.

    Parameters
    ----------
    flux_net: the flux of the source, less background flux 
        shape: [sources, apertures]
    area_ap: area of the aperture
        shape: [apertures]
    sigma_sky: error of the background flux
        shape: [sources]
    n_sky: number of background pixels used to calculate sigma_sky
    gain: gain of CCD
    readout_noise: readout noise of CCD
    
    sigma_Fnet = sqrt[ G*Fnet + Aap*sigma_sky^2 + Aap^2*sigma_sky^2/Nsky + Aap*RON^2 ]
    """
    
    # CCD Equation terms (Poisson noise + sky background noise + readout noise)
    variance = (flux_net*gain + 
                ( sigma_sky[:, None]**2 * area_ap[None, :]) + 
                (sigma_sky[:, None]**2 * area_ap[None, :]**2 / n_sky) + 
                (area_ap * readout_noise**2))
    
    # Return standard deviation (ensure no negative values under the root)
    return np.sqrt(np.maximum(variance, 0.0))

def annulus_sigma_clip_std(data, coords, r_in, r_out, sigma=3):
    """
    Compute the sigma-clipped background noise in an annulus around each coordinate
    using photutils.

    Adapted from photometry.annulus_sigma_clip_median in the Eloy library. (https://github.com/lgrcia/eloy)

    Parameters
    ----------
    data : np.ndarray
        2D image data.
    coords : np.ndarray
        Array of (x, y) coordinates.
    r_in : float
        Inner radius of the annulus.
    r_out : float
        Outer radius of the annulus.
    sigma : float, optional
        Sigma for sigma-clipping.

    Returns
    -------
    np.ndarray
        Array of background std values for each coordinate.
    """
    annulus = CircularAnnulus(coords, r_in, r_out)
    annulus_masks = annulus.to_mask(method="center")

    bkg_std = []
    for mask in annulus_masks:
        annulus_data = mask.multiply(data)
        if annulus_data is not None:
            annulus_data_1d = annulus_data[mask.data > 0]
            _, _, stdev_sigma_clipped = sigma_clipped_stats(annulus_data_1d, sigma=sigma)
            bkg_std.append(stdev_sigma_clipped)
        else:
            bkg_std.append(0.0)

    return np.array(bkg_std)
