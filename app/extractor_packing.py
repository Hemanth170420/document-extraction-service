import re


def extract_packing_fields(text):

    result = {
        "packing_list_number": None,
        "invoice_number": None,
        "ship_to_address": None,
        "line_items": []
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # ------------------------------
    # 1️⃣ Extract header fields
    # ------------------------------
    for i, line in enumerate(lines):
        if line.lower() == "packing list no:" and i + 1 < len(lines):
            result["packing_list_number"] = lines[i + 1]

        if line.lower() == "invoice no:" and i + 1 < len(lines):
            result["invoice_number"] = lines[i + 1]

        if line.lower() == "consignee:" and i + 1 < len(lines):
            result["ship_to_address"] = lines[i + 1]

    # ------------------------------
    # 2️⃣ Detect item number positions
    # ------------------------------
    item_indices = []

    for idx, line in enumerate(lines):
        if line.isdigit() and 1 <= int(line) <= 50:
            item_indices.append(idx)

    # ------------------------------
    # 3️⃣ Parse each item block
    # ------------------------------
    for k in range(len(item_indices)):

        start = item_indices[k]
        end = item_indices[k + 1] if k + 1 < len(item_indices) else len(lines)

        block = lines[start:end]

        item = {
            "item_no": block[0],
            "description": None,
            "hs_code": None,
            "quantity": None,
            "net_weight": None,
            "gross_weight": None
        }

        # Extract fields from block dynamically
        for line in block[1:]:

            # HS Code (6 digit number)
            if re.match(r"^\d{6}$", line):
                item["hs_code"] = line

            # Quantity
            elif "pcs" in line.lower():
                item["quantity"] = line

            # Weight (numeric only)
            elif re.match(r"^\d+$", line):
                if item["net_weight"] is None:
                    item["net_weight"] = line
                else:
                    item["gross_weight"] = line

            # Description
            elif item["description"] is None:
                item["description"] = line

        result["line_items"].append(item)

    return result