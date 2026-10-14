"""Validate and execute notebooks in fresh kernels using this Python environment.

By default the input files are not changed. Use --write to save executed outputs.
Only execute notebooks whose code you trust.
"""
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json
import os
import sys

import nbformat
from nbclient import NotebookClient


def execute(path, write=False):
    path = path.resolve()
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    with TemporaryDirectory(prefix="homework-kernel-") as temporary:
        kernel = Path(temporary) / "kernels" / "python3"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Homework validation", "language": "python",
        }), encoding="utf-8")
        search_path = temporary
        if os.environ.get("JUPYTER_PATH"):
            search_path += os.pathsep + os.environ["JUPYTER_PATH"]
        with patch.dict(os.environ, {"JUPYTER_PATH": search_path}):
            client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                                    allow_errors=False, record_timing=False,
                                    resources={"metadata": {"path": str(path.parent)}})
            client.execute()
    nbformat.validate(notebook)
    code_cells = [c for c in notebook.cells if c.cell_type == "code"]
    images = sum("image/png" in output.get("data", {})
                 for cell in code_cells for output in cell.get("outputs", []))
    errors = [output for cell in code_cells for output in cell.get("outputs", [])
              if output.output_type == "error"]
    if errors or any(c.execution_count is None for c in code_cells):
        raise AssertionError("Not every code cell executed successfully")
    if write:
        nbformat.write(notebook, path)
    print(f"PASS {path.name}: {len(code_cells)} code cells; {images} plot outputs; "
          + ("executed outputs saved" if write else "input file unchanged"), flush=True)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="+", type=Path)
    parser.add_argument("--write", action="store_true", help="Save outputs into the input notebooks")
    args = parser.parse_args()
    for path in args.notebooks:
        execute(path, write=args.write)


if __name__ == "__main__":
    main()
