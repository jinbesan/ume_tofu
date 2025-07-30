import gspread
from rapidfuzz import process
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ume-tofu-tracker-creds.json", scope)
gspread_client = gspread.authorize(creds)
sheet = gspread_client.open_by_key("1cu66ZGH9HkBEoLB2FMVyPOXS7PaZ7oxfLg9ba3VwD5E").sheet1
log_sheet = gspread_client.open_by_key("1cu66ZGH9HkBEoLB2FMVyPOXS7PaZ7oxfLg9ba3VwD5E").worksheet("Transaction Log")


def extract_items_from_message(message: str):
    return [item.strip() for item in message.split(",")]

def fuzzy_match(input_items, known_items, threshold=50):
    matched = []
    for item in input_items:
        match, score, _ = process.extractOne(item, known_items)
        if score >= threshold:
            matched.append(match)
        else:
            matched.append(None)
    return matched

def parse_item_quantity(part: str):
    pattern = r'^(.*?)\s*(?:[x×]?\s*(\d+))?$'
    match = re.match(pattern, part.strip())

    if not match:
        return None

    item = match.group(1).strip()
    quantity = int(match.group(2)) if match.group(2) else 1  # default to 1 if no quantity

    return item, quantity

def extract_items_and_quantities(message: str):
    parts = extract_items_from_message(message)
    items = []
    quantities = []
    
    for part in parts:
        parsed = parse_item_quantity(part)
        if parsed:
            item, quantity = parsed
            items.append(item)
            quantities.append(quantity)
        else:
            items.append(part.strip())
            quantities.append(1)  # default quantity if not specified
    
    return items, quantities


def log_transaction(user, items, total_price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp] + [user] + [total_price] + [", ".join([f"{item['name']} x{item['qty']}" for item in items])]
    log_sheet.append_row(row)

def restore_inventory(items, quantities):
    recovered_items = []
    recovered_quantities = []
    founds = []
    for item, quantity in zip(items, quantities):
        cell = sheet.find(item)
        found = False
        if cell:
            row = cell.row
            col = cell.col
            current_qty = sheet.cell(row, col + 2).numeric_value
            new_qty = current_qty - quantity
            sheet.update_cell(row, col + 2, new_qty) 
            found = True
        recovered_items.append(item)
        recovered_quantities.append(quantity)
        founds.append(found)
    return recovered_items, recovered_quantities, founds

def update_sheet(content: str, user: str = "Unknown User"):

    items, quantities = extract_items_and_quantities(content)

    sheet_data = sheet.get_all_records()
    item_names = [row["Character"] for row in sheet_data]
    results = []
    price = 0
    
    matched_items = fuzzy_match(items, item_names)
    
    for item_input, matched, quantity in zip(items, matched_items, quantities):
        if matched:

            cell = sheet.find(matched)
            row = cell.row if cell else None
            col = cell.col if cell else None
            if row is None:
                results.append(f"❌ '{item_input}' not found in the sheet")
                continue
            qty_cell = sheet.cell(row, col + 2).numeric_value
            current_qty = sheet.cell(row, col + 4).numeric_value
            price_cell = sheet.cell(row, col + 5, value_render_option='FORMULA').value
            

            if current_qty > 0:
                sheet.update_cell(row, 7, qty_cell + quantity)
                price += price_cell * quantity
                results.append(f"✅ {quantity}× {matched}: updated to {qty_cell + quantity}")
            else:
                results.append(f"⚠️ {matched}: out of stock!")
        else:
            results.append(f"❌ '{item_input}' not recognized")
    results.append(f"Total price: ${price}")

    log_transaction(user, [{"name": item, "qty": qty} for item, qty in zip(matched_items, quantities)], price)
    return results

def undo(user: str):
    records = log_sheet.get_all_records()
    for i in range(len(records)-1, -1, -1):
        entry = records[i]
        if entry["User"] == user:
            items, quantities = extract_items_and_quantities(entry["Items"])
            rcv_items, rcv_quantities, rcv_found = restore_inventory(items, quantities)
            status = []
            for item, quantity, found in zip(rcv_items, rcv_quantities, rcv_found):
                if found:
                    status.append(f"✅ {quantity}× {item} restored")
                else:
                    status.append(f"❌ {item} not found in the sheet")
            if all(rcv_found):
                log_sheet.delete_rows(i + 2)
                status.append("---------------------------------------------------")
                status.append("Transaction undone successfully.")
            else:
                status.append("Transaction could not be undone due to missing items.")
            break
            
    return status if len(status) > 0 else None