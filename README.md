# photometry-workflow

A command-line toolset and Python API for performing photometry workflows on sets of
astronomical images.

## Tools

| Command                 | Purpose                                        | API module                                    |
| ------------------------ | ----------------------------------------------- | ---------------------------------------------- |
| `photometry-screen`     | Screen and select images                       | `photometry_workflow.screening`               |
| `photometry-align`      | Align a sequence of images                     | `photometry_workflow.alignment`               |
| `photometry-aperture`   | Aperture photometry                            | `photometry_workflow.aperture_photometry`     |
| `photometry-compstars`  | Identify comparison stars                      | `photometry_workflow.comparison_stars`        |
| `photometry-diffphot`   | Differential photometry                        | `photometry_workflow.differential_photometry` |

Each command is a thin CLI wrapper around a callable API function of the same purpose,
so any step can be scripted directly in Python instead of invoked as a subprocess.

## Setup

```bash
micromamba env create -f environment.yaml
micromamba activate photometry
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

See [docs/project-structure.md](docs/project-structure.md) for how the codebase is laid
out and [docs/interface.md](docs/interface.md) for the CLI/API conventions each tool follows.
