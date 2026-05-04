# Docling Extraction Prompt

Create a Python client workflow that calls docling-serve over HTTP and stores extraction output.

## Requirements

- Implement a dedicated HTTP client module for docling-serve.
- Accept document input reference and extraction options.
- Save extraction output in both Markdown and JSON formats.
- Store outputs under `data/output/` using public-safe sample data.
- Add clear error handling for network and response failures.

## Constraints

- Treat docling-serve as an external service.
- Do not import or modify docling-serve internals.
- Keep code modular and typed with Pydantic where appropriate.

## Deliverables

- Client module
- Output writer module (Markdown + JSON)
- Minimal usage example
- Notes on required docling-serve endpoint configuration
