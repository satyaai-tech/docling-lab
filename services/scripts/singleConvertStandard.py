import gc
import json
import sys
import traceback
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions


def build_converter() -> DocumentConverter:
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,
        do_table_structure=True,
    )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )


def export_document(result, pdf_path: Path, output_dir: Path | None = None) -> None:
    doc = result.document

    base_dir = output_dir if output_dir else pdf_path.parent
    base_dir.mkdir(parents=True, exist_ok=True)

    base = base_dir / (pdf_path.stem + "_std")

    paths = {
        "JSON": base.with_suffix(".json"),
        "Markdown": base.with_suffix(".md"),
        "DocTags": base.with_suffix(".doctags"),
        "DocLang": base.with_suffix(".doclang"),
    }

    paths["JSON"].write_text(
        json.dumps(doc.export_to_dict(), indent=2),
        encoding="utf-8",
    )

    paths["Markdown"].write_text(
        doc.export_to_markdown(),
        encoding="utf-8",
    )

    paths["DocTags"].write_text(
        doc.export_to_doctags(),
        encoding="utf-8",
    )

    paths["DocLang"].write_text(
        doc.export_to_doclang(),
        encoding="utf-8",
    )

    for label, path in paths.items():
        print(f"Saved {label} to: {path}")


def main(pdf_path: Path, output_dir: Path | None = None) -> None:
    converter = None
    result = None

    try:
        converter = build_converter()

        result = converter.convert(str(pdf_path))

        export_document(result, pdf_path, output_dir)

    except Exception as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

    finally:
        del result
        del converter
        gc.collect()


if __name__ == "__main__":

    PDF_PATH = r"/Users/satyaanumolu/POCs/docling-lab/data/data/raw/loan-estimates/cfpb/201403_cfpb_loan-estimate_fixed-rate-loan-sample-H24B_pages_2-4.pdf"

    OUTPUT_DIR = Path(
        r"/Users/satyaanumolu/POCs/docling-lab/data/output/loan-estimates/cfpb"
    )

    main(Path(PDF_PATH), output_dir=OUTPUT_DIR)