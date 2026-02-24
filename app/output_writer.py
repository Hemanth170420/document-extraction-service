import os
import json
import pandas as pd


def write_output(data, input_path):
    """
    Writes extracted data into:
    - JSON file
    - Excel file (.xlsx)
    """

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Generate base filename from input file
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    json_path = os.path.join("output", f"{base_name}.json")
    excel_path = os.path.join("output", f"{base_name}.xlsx")

    # --------------------------------------------------
    # 1️⃣ Write JSON
    # --------------------------------------------------
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # --------------------------------------------------
    # 2️⃣ Write Excel
    # --------------------------------------------------
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

        # Metadata Sheet
        metadata = {k: v for k, v in data.items() if k != "line_items"}
        meta_df = pd.DataFrame(list(metadata.items()), columns=["Field", "Value"])
        meta_df.to_excel(writer, sheet_name="Metadata", index=False)

        # Line Items Sheet
        if "line_items" in data and data["line_items"]:
            line_df = pd.DataFrame(data["line_items"])
        else:
            # Create empty sheet if no line items found
            line_df = pd.DataFrame(columns=["description", "quantity", "price"])

        line_df.to_excel(writer, sheet_name="Line_Items", index=False)

    print("\n===== OUTPUT GENERATED =====")
    print(f"JSON Saved  → {json_path}")
    print(f"Excel Saved → {excel_path}")
