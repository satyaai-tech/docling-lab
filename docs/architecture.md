# Architecture

## Components

- **docling-serve**: Parsing and extraction service, run as an external app over HTTP.
- **label-studio**: Ground-truth labeling and annotation tool, used via UI/API exports.
- **extraction-api**: Custom orchestration API (FastAPI) that calls docling-serve.
- **evaluation-service**: Custom service that compares extraction output with ground truth.
- **data folders**: Store sample/synthetic inputs and outputs only.

## Service Boundaries

- Keep `apps/docling-serve` and `apps/label-studio` dependency-isolated.
- Do not import internal code from external apps into custom services.
- Custom services should define their own schemas, clients, and route logic.

## Data Flow

1. Input document reference enters extraction-api.
2. extraction-api calls docling-serve over HTTP.
3. extraction output is normalized and stored in `data/output/`.
4. Label Studio annotations are exported to `data/ground-truth/`.
5. evaluation-service compares outputs and emits simple metrics.

## Data Safety

- Commit only public-safe, sanitized sample data.
- Do not commit real private documents, secrets, or large generated artifacts.
