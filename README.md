# photometry-workflow

A command-line toolset and Python API for performing photometry workflows on sets of
astronomical images.

## Tools

| Command                 | Purpose                                        | API module                                    |
| ------------------------ | ----------------------------------------------- | ---------------------------------------------- |
| `pw-screen`     | Screen and select images                       | `photometry_workflow.screening`               |
| `pw-align`      | Align a sequence of images                     | `photometry_workflow.alignment`               |
| `pw-aperture`   | Aperture photometry                            | `photometry_workflow.aperture_photometry`     |
| `pw-compstars`  | Identify comparison stars                      | `photometry_workflow.comparison_stars`        |
| `pw-diffphot`   | Differential photometry                        | `photometry_workflow.differential_photometry` |

Each command is a thin CLI wrapper around a callable API function of the same purpose,
so any step can be scripted directly in Python instead of invoked as a subprocess.

## Setup

```bash
micromamba env create -f environment.yaml
micromamba activate photometry
pip install -e ".[dev]"
```

## Usage

Each command also accepts `--help` for the full list of options.

```bash
# Screen a directory of images and write the selected ones to a list
pw-screen raw/ -o selected.txt

# Align the selected images to a reference frame
pw-align $(cat selected.txt) -o aligned/ -r aligned/ref.fits

# Measure aperture photometry at one or more pixel positions
pw-aperture aligned/*.fits --position 512,480 --aperture-radius 8 -o target.ecsv

# Find comparison star candidates near the target on a reference image
pw-compstars aligned/ref.fits --target 512,480 -o comp_candidates.ecsv

# Compute a differential light curve from target and comparison photometry
pw-diffphot --target target.ecsv --comparison comp1.ecsv --comparison comp2.ecsv -o lightcurve.ecsv
```

## Running tests

```bash
pytest
```

See [docs/project-structure.md](docs/project-structure.md) for how the codebase is laid
out and [docs/interface.md](docs/interface.md) for the CLI/API conventions each tool follows.
