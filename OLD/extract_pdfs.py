import os
import pypdf

def extract_pdf_text(pdf_path, txt_path):
    print(f"Extracting {pdf_path} to {txt_path}...")
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"\n--- Page {i+1} ---\n"
            text += page.extract_text() or ""
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully extracted to {txt_path}")
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")

if __name__ == "__main__":
    extract_pdf_text("Cosmological Cavitation Data Analysis.pdf", "Cosmological_Cavitation_Data_Analysis.txt")
    extract_pdf_text("Exabyte Size and Its Scale.pdf", "Exabyte_Size_and_Its_Scale.txt")
