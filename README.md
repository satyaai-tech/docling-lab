# Docling Lab

Monorepo for experimenting with document extraction workflows using Docling and annotation workflows with Label Studio.

## Workspace Overview

```text
docling-lab/
├── apps/
│   ├── docling-serve/      # Docling Serve API app (uv project)
│   └── label-studio/       # Label Studio local app (uv project)
├── data/                   # Shared local datasets and files
├── notebooks/              # Research and experiment notebooks
└── services/
    ├── extraction-api/     # Planned API service (currently empty)
    └── extraction-service/ # Planned worker/service layer (currently empty)
```

## Prerequisites

- Python 3.12+
- uv

Install uv if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Start

From the repository root, set up each app:

```bash
cd apps/docling-serve && uv sync
cd ../label-studio && uv sync
```

## Run Apps

Use separate terminals for each app.

### 1) Docling Serve API

```bash
cd apps/docling-serve
uv run docling-serve run
```

Default endpoints:

- API: http://127.0.0.1:5001
- OpenAPI docs: http://127.0.0.1:5001/docs

Development mode with reload:

```bash
uv run docling-serve dev
```

### 2) Label Studio

```bash
cd apps/label-studio
uv run label-studio start --port 8080
```

Open:

- UI: http://localhost:8080

Optional local data directory:

```bash
LABEL_STUDIO_BASE_DATA_DIR=./.label-studio-data \
uv run label-studio start --host 0.0.0.0 --port 8080
```

## Project Notes

- Each app is managed independently with its own `pyproject.toml` and `uv.lock`.
- `apps/*/main.py` files are placeholders and are not required to launch Docling Serve or Label Studio.
- `services/extraction-api` and `services/extraction-service` are scaffolds reserved for future implementation.

## Helpful Commands

From each app directory:

```bash
uv sync
uv run --help
```

Label Studio reset (optional):

```bash
cd apps/label-studio
rm -rf ./.label-studio-data
```

## Next Steps

- Add service implementations under `services/`.
- Add notebooks to `notebooks/` for extraction and evaluation experiments.
- Add a top-level task runner (Makefile or justfile) for common commands.
