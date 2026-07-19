# Project structure

```
photometry-workflow/
├── pyproject.toml
├── environment.yaml
├── src/
│   └── photometry_workflow/
│       ├── common/                    # shared helpers used across tools (e.g. image path resolution)
│       ├── screening/                 # screening and selecting images
│       ├── alignment/                 # aligning a sequence of images
│       ├── aperture_photometry/       # aperture photometry
│       ├── comparison_stars/          # identifying comparison stars
│       └── differential_photometry/   # differential photometry
└── tests/                             # one test module per tool, plus common/
```

Each tool package follows the same two-file layout:

- `api.py` — the callable Python API: plain functions taking/returning Python and
  astropy objects (`Path`, `Table`, etc). No argument parsing, no I/O side effects
  beyond what the function is explicitly asked to do.
- `cli.py` — an argparse-based `build_parser()` and `main()` that parses terminal
  arguments, reads/writes files, and calls into `api.py` for the actual logic.

`pyproject.toml` registers one console-script entry point per tool (e.g.
`photometry-screen`), each pointing at that tool's `cli.main`.
