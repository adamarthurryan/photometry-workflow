# Notebooks

Jupyter notebooks for interactively experimenting with the photometry calculations —
particularly apparent magnitude and differential photometry — ahead of settling on an
implementation in the `photometry_workflow` package. Not part of the installable
package; nothing under `src/` imports from here.

Each notebook reads the `sources`/`images`/`flux` tables written by `pw-aperture` (see
`../reduce/` or wherever you pointed `-o`) and works from there. Run them with the
`photometry` micromamba environment's kernel ("Python 3 (ipykernel)").

- `apparent_magnitude.ipynb` — per-image zero-point calibration against Gaia-matched
  sources, applied to get a light curve for a single source.
