# Local Workflow

## 1. Run docling-serve

```bash
cd apps/docling-serve
uv sync
uv run docling-serve run
```

## 2. Run label-studio

```bash
cd apps/label-studio
uv sync
uv run label-studio start --port 8080
```

## 3. Call extraction API

Run your custom extraction API service (in `services/`) and send extraction requests that call docling-serve over HTTP.

## 4. Export Label Studio annotations

Export labeling results from Label Studio and place normalized artifacts in `data/ground-truth/`.

## 5. Run evaluation

Execute evaluation logic to compare extraction output in `data/output/` with ground truth in `data/ground-truth/`.

## 6. Review results

Use generated metric summaries and notebooks to inspect quality trends and identify schema or mapping improvements.

## Notes

- Keep each service dependency-isolated.
- Use synthetic/sanitized data only.
- Keep runs reproducible with concise README instructions in each service.
