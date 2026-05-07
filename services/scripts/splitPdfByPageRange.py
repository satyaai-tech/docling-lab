import argparse
import sys
import traceback
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError as exc:
    print(
        "Missing dependency: pypdf. Install it with `pip install pypdf`.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


def build_output_path(pdf_path: Path, from_page: int, to_page: int) -> Path:
    return pdf_path.with_name(f"{pdf_path.stem}_pages_{from_page}-{to_page}.pdf")


def split_pdf(pdf_path: Path, from_page: int, to_page: int) -> Path:
    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)

    if from_page < 1 or to_page < 1:
        raise ValueError("from_page and to_page must be >= 1.")
    if from_page > to_page:
        raise ValueError("from_page must be less than or equal to to_page.")
    if to_page > total_pages:
        raise ValueError(
            f"Requested page range {from_page}-{to_page} exceeds total pages ({total_pages})."
        )

    writer = PdfWriter()
    for page_index in range(from_page - 1, to_page):
        writer.add_page(reader.pages[page_index])

    output_path = build_output_path(pdf_path, from_page, to_page)
    with output_path.open("wb") as out_file:
        writer.write(out_file)

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split a PDF by page range and save output in the same directory."
    )
    parser.add_argument("pdf_path", help="Absolute or relative path to the input PDF.")
    parser.add_argument("from_page", type=int, help="1-based start page (inclusive).")
    parser.add_argument("to_page", type=int, help="1-based end page (inclusive).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf_path).expanduser().resolve()

    if not pdf_path.exists():
        print(f"Input PDF not found: {pdf_path}", file=sys.stderr)
        return 1
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Input file is not a PDF: {pdf_path}", file=sys.stderr)
        return 1

    try:
        output_path = split_pdf(pdf_path, args.from_page, args.to_page)
        print(f"Created: {output_path}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to split PDF: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())