import sys
import os
from app.validator import validate_invoice, validate_packing
from app.ocr import run_ocr
from app.classifier import classify_document
from app.extractor_invoice import extract_invoice_fields
from app.extractor_packing import extract_packing_fields
from app.output_writer import write_output


def main(path):

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    try:
        # --------------------------------------------------
        # 1️⃣ Run OCR
        # --------------------------------------------------
        print("\n===== RUNNING OCR =====")
        text = run_ocr(path)
        print("\n===== RAW OCR TEXT =====\n")
        print(text)
        print("\n===== END OCR TEXT =====\n")
        # Save raw OCR text (for debugging)
        with open("output/raw_text.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print("Raw OCR output saved → output/raw_text.txt")

        # --------------------------------------------------
        # 2️⃣ Classify Document
        # --------------------------------------------------
        doc_type, confidence = classify_document(text)

        print("\n===== DOCUMENT CLASSIFICATION =====")
        print("Detected Type:", doc_type)
        print("Confidence Score:", confidence)

        # --------------------------------------------------
        # 3️⃣ Extract Fields Based on Type
        # --------------------------------------------------
        if doc_type == "invoice":
            extracted_data = extract_invoice_fields(text)
            warnings = validate_invoice(extracted_data)

        elif doc_type == "packing_list":
            extracted_data = extract_packing_fields(text)
            warnings = validate_packing(extracted_data)

        else:
            extracted_data = {"document_type": "unknown", "line_items": []}
            warnings = ["Unknown document type"]

# Print warnings
        if warnings:
            print("\n===== VALIDATION WARNINGS =====")
            for w in warnings:
                print("-", w)

        extracted_data["document_type"] = doc_type
        extracted_data["classification_confidence"] = confidence

        write_output(extracted_data, path)

        print("\n===== PROCESS COMPLETED SUCCESSFULLY =====")

    except Exception as e:
        print("\nERROR:", e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.main <file_path>")
        sys.exit()

    file_path = sys.argv[1]
    main(file_path)
