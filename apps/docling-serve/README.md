# Docling Serve App

Small `uv` project for running [Docling Serve](https://pypi.org/project/docling-serve/) locally as an API service.

## Requirements

- Python 3.12
- `uv`

## Setup

From this app directory:

```bash
cd apps/docling-serve
uv sync
```

## Run

Start the Docling Serve API:

```bash
uv run docling-serve run
```

By default, the service is available at:

- API: http://127.0.0.1:5001
- API docs: http://127.0.0.1:5001/docs

For a development server with reload enabled:

```bash
uv run docling-serve dev
```

## Project Files

- `pyproject.toml` defines the Python project and the `docling-serve` dependency.
- `.python-version` pins the local Python version to 3.12.
- `uv.lock` locks the resolved dependency graph.
- `main.py` is currently a placeholder entrypoint for this app.
