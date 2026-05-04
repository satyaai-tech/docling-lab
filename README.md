# docling-lab

Local lab for building and evaluating document extraction workflows with clear service boundaries.

This repository is designed for experimentation and portfolio-friendly engineering practices:

- Run `docling-serve` as an out-of-the-box extraction service.
- Run `label-studio` as an out-of-the-box annotation/ground-truth tool.
- Build custom FastAPI services for orchestration and evaluation.
- Track extraction quality against synthetic or sanitized ground truth.

## Architecture Guardrails

- Treat `apps/docling-serve` and `apps/label-studio` as external apps.
- Do not mix dependencies across unrelated apps/services.
- Use separate environments and dependency files per app/service.
- Call Docling Serve and Label Studio over HTTP instead of importing internals.
- Keep committed artifacts public-safe and lightweight.

## Repository Structure

```text
docling-lab/
├── .github/
│   └── copilot-instructions.md
├── agents/                         # Agent role definitions for architecture/evaluation
├── apps/
│   ├── docling-serve/              # External app wrapper (uv project)
│   └── label-studio/               # External app wrapper (uv project)
├── data/
│   ├── input/                      # Local/synthetic sample inputs (gitignored)
│   ├── output/                     # Generated outputs/metrics (gitignored)
│   └── ground-truth/               # Ground truth artifacts (gitignored)
├── docs/                           # Workflow, architecture, and git setup notes
├── docling-wrapper/                # Single FastAPI wrapper service for docling-serve
├── notebooks/                      # Evaluation and analysis notebooks
├── prompts/                        # Reusable prompt templates
├── skills/                         # Implementation skill playbooks
└── (no services/ folder)           # Keep architecture simple with one wrapper service
```

## Prerequisites

- Python 3.12+
- uv

Install uv if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Run docling-serve

```bash
cd apps/docling-serve
uv sync
uv run docling-serve run
```

Default endpoints:

- API: http://127.0.0.1:5001
- OpenAPI docs: http://127.0.0.1:5001/docs

Dev mode with reload:

```bash
uv run docling-serve dev
```

## Run label-studio

```bash
cd apps/label-studio
uv sync
uv run label-studio start --port 8080
```

UI endpoint:

- http://localhost:8080

Optional local data directory inside the app folder:

```bash
LABEL_STUDIO_BASE_DATA_DIR=./.label-studio-data \
uv run label-studio start --host 0.0.0.0 --port 8080
```

## How Custom Services Should Integrate

The wrapper service in `docling-wrapper/` should act as the orchestration layer:

1. Accept a request with document reference and extraction schema/profile.
2. Call Docling Serve HTTP endpoints for extraction.
3. Optionally enrich or map outputs to your own Pydantic schemas.
4. Optionally pull or compare labels exported from Label Studio.
5. Write evaluation-ready artifacts to `data/output/`.

Do not add direct code-level coupling to upstream apps.

## Adding New Extraction Schemas

Recommended approach:

1. Define a versioned Pydantic model for the target schema in the wrapper service.
2. Add mapping/normalization logic from raw extraction output to the schema model.
3. Add validation checks for required fields and data types.
4. Store a small synthetic example input and expected output for regression checks.
5. Document schema version and usage in `docling-wrapper/README.md`.

## Evaluating Extraction Quality

Suggested workflow:

1. Store sanitized or synthetic reference labels in `data/ground-truth/`.
2. Run extraction and write normalized outputs to `data/output/`.
3. Compare predicted vs ground-truth fields with deterministic rules.
4. Produce field-level metrics and aggregate summaries.
5. Review trends in notebooks and iterate on extraction/schema mapping.

## Development Setup Files Added

- Copilot guidance: `.github/copilot-instructions.md`
- Prompt templates: `prompts/`
- Implementation playbooks: `skills/`
- Agent role definitions: `agents/`
- Supporting docs: `docs/`

See `docs/development-workflow.md` and `docs/service-architecture.md` for detailed guidance.
