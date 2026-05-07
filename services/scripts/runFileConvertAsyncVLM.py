import sys
import traceback
import gc
import json
from pathlib import Path

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    VlmPipelineOptions,
    VlmConvertOptions,
)
from docling.datamodel.vlm_engine_options import ApiVlmEngineOptions
from docling.datamodel.stage_model_specs import VlmModelSpec
from docling.pipeline.vlm_pipeline import VlmPipeline


PDF_PATH = r"/Users/satyaanumolu/POCs/docling-lab/data/data/raw/loan-estimates/cfpb/201403_cfpb_loan-estimate_fixed-rate-loan-sample-H24B_pages_2-4.pdf"

# Equivalent of vlm_pipeline_custom_config
vlm_options = VlmConvertOptions(
    model_spec=VlmModelSpec(
        name="granite_docling_ollama",
        default_repo_id="ibm/granite-docling:258m",
        prompt=(
            "Convert this document page to Docling DocTags. "
            "Preserve layout, text, tables, and reading order. "
            "Return only DocTags."
        ),
        response_format="doctags",
    ),

    engine_options=ApiVlmEngineOptions(
        engine_type="api",

        # equivalent of:
        # http://host.docker.internal:11434/v1/chat/completions
        #
        # because Python runs locally, use localhost
        url="http://localhost:11434/v1/chat/completions",

        headers={
            "Authorization": "Bearer ollama"
        },

        params={
            "model": "ibm/granite-docling:258m",
            "temperature": 0,
            "max_tokens": 4000,
        },
    ),
)

pipeline_options = VlmPipelineOptions(
    enable_remote_services=True,

    # equivalent of:
    # ocr=true
    do_ocr=True,
    

    # equivalent of:
    # tables=true
    do_table_structure=True,

    vlm_options=vlm_options,
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=VlmPipeline,
            pipeline_options=pipeline_options,
        )
    }
)

result = None

try:
    result = converter.convert(PDF_PATH)

    # Export multiple representations from the converted document.
    output_dict = result.document.export_to_dict()
    output_markdown = result.document.export_to_markdown()
    output_doctags = result.document.export_to_doctags()
    output_doclang = result.document.export_to_doclang()

    doc_json_text = json.dumps(output_dict, indent=2)

    pdf_path = Path(PDF_PATH)
    output_base = pdf_path.with_suffix("")
    json_path = output_base.with_suffix(".json")
    markdown_path = output_base.with_suffix(".md")
    doctags_path = output_base.with_suffix(".doctags")
    doclang_path = output_base.with_suffix(".doclang")

    json_path.write_text(doc_json_text, encoding="utf-8")
    markdown_path.write_text(output_markdown, encoding="utf-8")
    doctags_path.write_text(output_doctags, encoding="utf-8")
    doclang_path.write_text(output_doclang, encoding="utf-8")

    print(f"Saved JSON to: {json_path}")
    print(f"Saved Markdown to: {markdown_path}")
    print(f"Saved DocTags to: {doctags_path}")
    print(f"Saved DocLang to: {doclang_path}")
except Exception as exc:  # noqa: BLE001
    print(f"Conversion failed: {exc}", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)
finally:
    # Trigger model cleanup while logging is still initialized.
    del result
    del converter
    gc.collect()