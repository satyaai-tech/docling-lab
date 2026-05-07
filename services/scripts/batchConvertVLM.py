import gc
import json
import sys
import time
import traceback
from collections.abc import Iterable
from pathlib import Path

from docling.datamodel.base_models import ConversionStatus, InputFormat
from docling.datamodel.document import ConversionResult
from docling.datamodel.pipeline_options import VlmConvertOptions, VlmPipelineOptions
from docling.datamodel.stage_model_specs import VlmModelSpec
from docling.datamodel.vlm_engine_options import ApiVlmEngineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline


def build_converter() -> DocumentConverter:
    vlm_options = VlmConvertOptions(
        model_spec=VlmModelSpec(
            name="granite_docling_ollama",
            default_repo_id="ibm/granite-docling:258m",
            prompt=(
                "Convert this document page to Docling DocTags. "
                "Preserve layout, text, checkboxes, tables, and reading order. "
                "Return only DocTags."
            ),
            response_format="doctags",
        ),
        engine_options=ApiVlmEngineOptions(
            engine_type="api",
            # Use localhost when running Python directly (not inside Docker)
            url="http://localhost:11434/v1/chat/completions",
            headers={"Authorization": "Bearer ollama"},
            params={
                "model": "ibm/granite-docling:258m",
                "temperature": 0,
                "max_tokens": 4000,
            },
        ),
    )

    pipeline_options = VlmPipelineOptions(
        enable_remote_services=True,
        do_ocr=True,
        do_table_structure=True,
        vlm_options=vlm_options,
    )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls=VlmPipeline,
                pipeline_options=pipeline_options,
            )
        }
    )


def export_documents(
    conv_results: Iterable[ConversionResult],
    output_dir: Path | None = None,
) -> tuple[int, int, int]:
    success_count = 0
    failure_count = 0
    partial_success_count = 0

    for conv_res in conv_results:
        if conv_res.status == ConversionStatus.SUCCESS:
            success_count += 1
            src = conv_res.input.file
            base_dir = output_dir if output_dir else src.parent
            base_dir.mkdir(parents=True, exist_ok=True)
            base = base_dir / src.stem

            paths = {
                "JSON":     base.with_suffix(".json"),
                "Markdown": base.with_suffix(".md"),
                "DocTags":  base.with_suffix(".doctags"),
                "DocLang":  base.with_suffix(".doclang"),
            }

            try:
                doc = conv_res.document
                paths["JSON"].write_text(json.dumps(doc.export_to_dict(), indent=2), encoding="utf-8")
                paths["Markdown"].write_text(doc.export_to_markdown(), encoding="utf-8")
                paths["DocTags"].write_text(doc.export_to_doctags(), encoding="utf-8")
                paths["DocLang"].write_text(doc.export_to_doclang(), encoding="utf-8")

                for label, path in paths.items():
                    print(f"Saved {label} to: {path}")

            except Exception as exc:  # noqa: BLE001
                print(f"Export failed for '{src.name}': {exc}", file=sys.stderr)
                traceback.print_exc()
                failure_count += 1
                success_count -= 1

        elif conv_res.status == ConversionStatus.PARTIAL_SUCCESS:
            partial_success_count += 1
            print(f"Partial conversion for '{conv_res.input.file}':", file=sys.stderr)
            for item in conv_res.errors:
                print(f"\t{item.error_message}", file=sys.stderr)
        else:
            failure_count += 1
            print(f"Failed to convert '{conv_res.input.file}'.", file=sys.stderr)

    print(
        f"Processed {success_count + partial_success_count + failure_count} docs — "
        f"{success_count} succeeded, {partial_success_count} partial, {failure_count} failed."
    )
    return success_count, partial_success_count, failure_count


def main(input_paths: list[Path], output_dir: Path | None = None) -> None:
    converter = None

    try:
        converter = build_converter()
        start = time.time()

        conv_results = converter.convert_all(
            input_paths,
            raises_on_error=False,
        )

        _success, _partial, failure_count = export_documents(conv_results, output_dir=output_dir)

        elapsed = time.time() - start
        print(f"Batch conversion complete in {elapsed:.2f} seconds.")

        if failure_count > 0:
            sys.exit(1)

    except Exception as exc:  # noqa: BLE001
        print(f"Batch conversion failed: {exc}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
    finally:
        del converter
        gc.collect()


if __name__ == "__main__":
    INPUT_DIR = Path(r"/Users/satyaanumolu/POCs/docling-lab/data/data/raw/loan-estimates/cfpb")
    OUTPUT_DIR = Path(r"/Users/satyaanumolu/POCs/docling-lab/data/output/loan-estimates/cfpb")

    pdf_paths = list(INPUT_DIR.glob("*.pdf"))
    main(pdf_paths, output_dir=OUTPUT_DIR)
