# Evaluation Pipeline Prompt

Build an evaluation workflow to compare Docling extraction output with Label Studio ground truth.

## Requirements

- Load normalized extraction output from `data/output/`.
- Load ground truth exports from `data/ground-truth/`.
- Compare fields with deterministic matching logic.
- Produce simple metrics such as match rate and field-level accuracy.
- Emit machine-readable summary JSON.

## Constraints

- Keep datasets synthetic or sanitized.
- Keep implementation modular and testable.
- Do not include private or company-specific data.

## Deliverables

- Evaluation module(s)
- Metric summary output format
- Basic test cases for scoring logic
- README snippet showing how to run evaluation
