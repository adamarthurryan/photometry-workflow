Estimates the calibrated apparent magnitude of each source in each image, using the
sources, images, and flux tables produced by aperture photometry.

Inputs:
 - source, image and flux tables produced by the aperature photometry module
 - a configuration file specifying target, comparison, and check stars (by name and/or ra, dec)

Need to experiment with different methods of computing outputs:
  1. average across all sources and images to get target and check star magnitudes
    - use statistics such as source flux std to weight source contributions to magnitudes
    - maybe use iterative minimization of check star magnitude variance
  2. use specified comparison stars
  3. select comparison stars from sources using data from the Gaia photometry such as color  and magnitude differences

Outputs should propigate error measurements from the sources