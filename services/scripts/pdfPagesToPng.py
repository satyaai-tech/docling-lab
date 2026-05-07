import argparse
import sys
import traceback
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError as exc:
    print(
        "Missing dependency: PyMuPDF. Install it with pip install pymupdf.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert each page of a PDF into PNG files in the same directory."
    )
    parser.add_argument("pdf_path", help="Absolute or relative path to the input PDF.")
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Render resolution in DPI (default: 200).",
    )
    return parser.parse_args()


def validate_input(pdf_path: Path, dpi: int) -> None:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Input file is not a PDF: {pdf_path}")
    if dpi <= 0:
        raise ValueError("DPI must be greater than 0.")


def convert_pdf_pages_to_png(pdf_path: Path, dpi: int) -> list[Path]:
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)

    output_paths: list[Path] = []
    width = max(3, len(str(doc.page_count)))

    for page_idx in range(doc.page_count):
        page = doc.load_page(page_idx)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        output_path = pdf_path.with_name(
            f"{pdf_path.stem}_page_{page_idx + 1:0{width}d}.png"
        )
        pix.save(output_path)
        output_paths.append(output_path)

    doc.close()
    return output_paths


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf_path).expanduser().resolve()

    try:
        validate_input(pdf_path, args.dpi)
        output_paths = convert_pdf_pages_to_png(pdf_path, args.dpi)

        print(f"Converted {len(output_paths)} pages from: {pdf_path}")
        for path in output_paths:
            print(f"Created: {path}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to convert PDF pages: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())