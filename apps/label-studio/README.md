# Label Studio (Local App)

This folder runs Label Studio using `uv` and the dependency declared in `pyproject.toml`.

## Prerequisites

- Python 3.12+
- `uv` installed

## Setup

From this directory:

```bash
cd apps/label-studio
uv sync
```

## Run Label Studio

```bash
uv run label-studio start --port 8080
```

Open: `http://localhost:8080`

## Run with Host + Data Directory

```bash
LABEL_STUDIO_BASE_DATA_DIR=./.label-studio-data \
uv run label-studio start --host 0.0.0.0 --port 8080
```

This keeps local project state inside this app folder.

## Stop

Press `Ctrl+C` in the terminal running Label Studio.

## Optional: Reset Local State

If you want a clean start, remove local state and start again:

```bash
rm -rf ./.label-studio-data
```

## Quick Checks

- Show Label Studio CLI help:

	```bash
	uv run label-studio --help
	```

- If `uv run label-studio start` fails, re-sync dependencies:

	```bash
	uv sync
	```
