from pathlib import Path
from app.ingestion.parser.pdf_parser import PDFParser

parser = PDFParser()

pdf_path = Path("../data/raw/central_bank/banks.pdf")

text = parser.parse(pdf_path)

print(f"Characters: {len(text)}")
print("-" * 40)
print(text[:1000])