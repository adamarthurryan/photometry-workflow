Performs aperature photometry on all sources in the reference image, for each of the input images.

Inputs:
 - a list of images
 - a reference image

Outputs (three normalized tables, linked by id columns):
 - source_table: one row per reference-image source, keyed by `source_id`, cross-matched to Gaia photometry
 - image_table: one row per input image, keyed by `image_id`, with per-image measurements (time, alignment offset, fwhm)
 - flux_table: one row per (image, source) pair, referencing `image_id` and `source_id`, with flux and background measurements