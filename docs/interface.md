# CLI / API interface conventions

Every tool exposes the same functionality twice, and the two must stay in sync:

- **Terminal command** — a console-script (e.g. `photometry-align`) for use in shell
  pipelines and scripts.
- **Python API function** — a plain function in the tool's `api.py`, importable and
  callable directly (e.g. `photometry_workflow.alignment.api.align_images(...)`).

## Separation of concerns

- `api.py` contains all program logic. Functions accept and return Python/astropy
  objects (`pathlib.Path`, `astropy.table.Table`, tuples of floats, etc.), never raw
  strings that need further parsing, and never call `print` or `sys.exit`.
- `cli.py` contains all argument parsing and I/O. It is responsible for:
  - building an `argparse.ArgumentParser` via a `build_parser()` function (kept
    separate from `main()` so tests can exercise argument parsing without running
    the tool),
  - converting parsed string arguments into the types the API expects
    (e.g. `"10,20"` → `(10.0, 20.0)`),
  - reading input files and writing output files,
  - calling the corresponding `api.py` function to do the actual work.

## Conventions

- Image path arguments accept either individual files or directories (expanded via
  `photometry_workflow.common.io.resolve_image_paths`).
- Tabular results (photometry measurements, candidate lists, light curves) are
  `astropy.table.Table` objects, written with `Table.write(path, overwrite=True)`
  so the output format is inferred from the file extension (e.g. `.ecsv`, `.csv`, `.fits`).
- Pixel positions are passed on the command line as `"x,y"` and parsed into
  `(float, float)` tuples before reaching the API layer.
