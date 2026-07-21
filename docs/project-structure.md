# Project structure


Each tool package follows the same two-file layout:

- `api.py` — the callable Python API: plain functions taking/returning Python and
  astropy objects (`Path`, `Table`, etc). No argument parsing, no I/O side effects
  beyond what the function is explicitly asked to do.
- `cli.py` — an argparse-based `build_parser()` and `main()` that parses terminal
  arguments, reads/writes files, and calls into `api.py` for the actual logic.

`pyproject.toml` registers one console-script entry point per tool (e.g.
`pw-screen`), each pointing at that tool's `cli.main`.

`notebooks/` sits outside `src/` and this layout entirely — it's Jupyter notebooks for
experimenting with calculations against real tool output, not installable package code.
