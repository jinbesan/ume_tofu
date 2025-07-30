import re
import gspread
from rapidfuzz import process
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

items = ["Character1", "Character2", "Character3"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ume-tofu-tracker-creds.json", scope)
gspread_client = gspread.authorize(creds)
sheet = gspread_client.open_by_key("1cu66ZGH9HkBEoLB2FMVyPOXS7PaZ7oxfLg9ba3VwD5E").sheet1

sheet_data = sheet.get_all_records()

item_names = [row["Character"] for row in sheet_data]
sheet_data = sheet.get_all_records()
results = []
price = 0

print (sheet_data[0])



