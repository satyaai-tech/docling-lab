# docling-lab — Project Plan

> Status: Draft for iteration (no implementation yet)

## 1. Goal

Build a local-first document extraction pipeline with clear service boundaries.

Core stack:

- Docling Serve for parsing (OCR, layout, tables, structure)
- Ollama for all LLM inference
- Granite as default extraction model
- Optional reasoning model for validation/fallback
- Label Studio for ground-truth annotation
- Custom FastAPI service(s) for orchestration and evaluation

## 2. Non-Goals

- No direct code-level coupling to Docling Serve or Label Studio internals
- No external hosted LLM APIs in the baseline architecture
- No private/company documents or secrets in repository artifacts

## 3. High-Level Architecture

```text
Input Document
   -> Docling Serve (OCR + layout + table extraction)
   -> Normalized Document Payload
   -> Extraction Orchestrator API
      -> Granite (primary extraction)
      -> Optional Reasoning Model (validation/fallback)
   -> Final Structured Output
   -> Evaluation Service
      -> compare with Label Studio ground truth
   -> Metrics + review artifacts
```

## 4. Major Components

| Component | Purpose | Boundary |
|---|---|---|
| Docling Serve | Parse documents into structured content | External service over HTTP |
| Granite model (Ollama) | Primary extraction/classification/summarization | Called via Ollama API |
| Reasoning model (Ollama) | Validation, ambiguity resolution, fallback | Called conditionally via Ollama API |
| Extraction API | Orchestrate parsing + model flow + schema normalization | Custom FastAPI service |
| Label Studio | Ground-truth creation and export | External service/UI + export artifacts |
| Evaluation Service | Score predictions vs ground truth | Custom service or module |

## 5. Pipeline Stages

1. Ingest document reference and run metadata.
2. Parse document using Docling Serve.
3. Normalize parse output to a stable internal schema.
4. Run Granite for primary field extraction.
5. Optionally route to reasoning model for validation/fallback.
6. Persist structured output and provenance metadata.
7. Evaluate against Label Studio ground truth.
8. Produce run-level metrics and error breakdown.

## 6. Model Strategy

Primary rule:

- Docling parses, Granite extracts, reasoning model validates/fallbacks.

Routing policy (draft):

- Granite-only when extraction confidence and schema checks pass.
- Invoke reasoning model when confidence is low, fields conflict, or required fields fail validation.
- Keep model names configuration-driven and swappable.

## 7. Service Boundary Decision (Current)

Preferred initial shape:

- Single `services` FastAPI wrapper service for orchestration + Docling calls.
- Evaluation logic can live as a module/endpoint in the same service until complexity grows.

Deferred decision:

- Split into separate services only if throughput, async jobs, or deployment boundaries require it.

## 8. Data Contracts (Planning Level)

Normalized document payload should include:

- document metadata (id, source, type)
- extracted text blocks with page/region references
- table structures
- layout regions/reading-order hints
- parser/model provenance

Final extraction payload should include:

- schema version
- extracted fields
- confidence signals
- validation outcomes
- run metadata (model versions, timestamps)

## 9. Evaluation Approach (ParseBench-Inspired)

Use a capability-oriented evaluation strategy rather than a single generic accuracy score.

### 9.1 Capability Dimensions

- **Tables**: structural fidelity, header alignment, merged-cell correctness.
- **Content Faithfulness**: omissions, hallucinations, and reading-order integrity.
- **Semantic Formatting**: preservation of meaning-bearing formatting (e.g., emphasis, superscripts/subscripts, section/title structure).
- **Visual Grounding**: traceability of extracted elements back to page-level source locations.
- **Charts (Optional Phase 2)**: numeric value and label correctness for chart-heavy documents.

### 9.2 Metric Strategy

- Report **per-dimension metrics** first, then a composite score.
- Keep baseline metrics deterministic and reproducible.
- Use mixed metric types where needed:
   - pass-rate style metrics for rule-based checks
   - continuous metrics for structural quality (especially tables)

### 9.3 Dataset Protocol

- Build a stratified evaluation set covering multiple document types and difficulty levels.
- Keep fixed split/versioning for reproducibility.
- Use only public-safe, sanitized, or synthetic documents.

### 9.4 Run Protocol

- Evaluate each pipeline variant on the same dataset slice.
- Record run metadata: Docling settings, Ollama model names/versions, schema version, and evaluation version.
- Persist both summary metrics and per-document error artifacts for regression analysis.

### 9.5 Quality Gates

- Define minimum thresholds per capability dimension (not only overall score).
- Promote a pipeline iteration only when all critical dimensions pass.
- Route failures to targeted remediation:
   - table failures -> parser/table configuration review
   - faithfulness failures -> normalization/extraction prompt review
   - grounding failures -> provenance/layout mapping review

### 9.6 Baseline Error Taxonomy

- missing
- mismatch
- format
- grounding
- unsupported

### 9.7 Composite Score (Planning Rule)

- Keep a composite score for trend tracking and quick comparisons.
- Do not use composite score alone for go/no-go decisions.
- Final decision must include per-dimension threshold checks.

## 10. Open Questions

- Which Docling model settings should be default for this repo?
- Which Granite variant should be baseline on Ollama?
- Which reasoning model should be default fallback?
- What confidence/validation thresholds trigger fallback?
- Should evaluation run as separate service or module first?
- Should Label Studio ingestion be manual export first, then API sync later?

## 11. Iteration Checklist

- [ ] Confirm baseline model lineup (Docling config + Granite + reasoning model)
- [ ] Finalize single-service boundaries and criteria for future split
- [ ] Freeze normalized payload contract v1
- [ ] Freeze evaluation metrics v1
- [ ] Define minimal experiment matrix for model comparison
