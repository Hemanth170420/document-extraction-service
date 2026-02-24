import re


def extract_invoice_fields(text):

    result = {
        "vendor_name": None,
        "invoice_number": None,
        "invoice_date": None,
        "line_items": []
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    text_lower = text.lower()

    # ------------------------------
    # 1️⃣ Invoice Number
    # ------------------------------
    match = re.search(r"invoice\s*no[:\s]*([a-z0-9\-\/]+)", text_lower)
    if match:
        result["invoice_number"] = match.group(1)

    # ------------------------------
    # 2️⃣ Invoice Date
    # ------------------------------
    match = re.search(r"date\s*(of issue)?[:\s]*([0-9\/\-\.]+)", text_lower)
    if match:
        result["invoice_date"] = match.group(match.lastindex)

    # ------------------------------
    # 3️⃣ Vendor Name (After Seller:)
    # ------------------------------
    # ------------------------------
# 3️⃣ Vendor Name (Improved)
# ------------------------------
    for i, line in enumerate(lines):
        if line.lower() == "seller:":
        # Skip labels like "Client:"
            j = i + 1
            while j < len(lines):
                if not lines[j].lower().endswith(":"):
                    result["vendor_name"] = lines[j]
                    break
                j += 1
            break

    # ------------------------------
    # 4️⃣ Block-Based Table Parsing
    # ------------------------------
    i = 0
    while i < len(lines):

        # Detect item number like "1."
        if re.match(r"^\d+\.$", lines[i]):

            item = {
                "item_no": lines[i].replace(".", ""),
                "description": "",
                "quantity": None,
                "unit": None,
                "net_price": None,
                "gross_price": None
            }

            i += 1

            # Collect description lines until numeric value appears
            description_lines = []
            while i < len(lines) and not re.match(r"^\d+[,\.]?\d*$", lines[i]):
                description_lines.append(lines[i])
                i += 1

            item["description"] = " ".join(description_lines)

            # Now extract next known fields safely
            if i < len(lines):
                item["quantity"] = lines[i]
                i += 1

            if i < len(lines):
                item["unit"] = lines[i]
                i += 1

            if i < len(lines):
                item["net_price"] = lines[i]
                i += 1

            # Skip net worth + VAT
            i += 2

            if i < len(lines):
                item["gross_price"] = lines[i].replace(" ","")
                i += 1

            result["line_items"].append(item)

        else:
            i += 1

    return result