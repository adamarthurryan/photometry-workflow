Estimates the calibrated apparent magnitude of each source in each image, using the
sources, images, and flux tables produced by aperture photometry.

Inputs:
 - source_table: one row per reference-image source, keyed by `source_id`, cross-matched to Gaia photometry
 - image_table: one row per input image, keyed by `image_id`
 - flux_table: one row per (image, source) pair, referencing `image_id` and `source_id`

Outputs:
 - a table of estimated apparent magnitude for each (image, source) pair, calibrated
   per image against the sources with a Gaia magnitude match (`gaia_matched`)
