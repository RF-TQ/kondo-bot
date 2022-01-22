import os
from dotenv import load_dotenv
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json

# Load credentials
load_dotenv()
json_data = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')

# Get TL document
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_data, scope)
client = gspread.authorize(creds)
sheet = client.open('Kondo Bot Sheet')

def get_sheet(sheet_name):
    return sheet.worksheet(sheet_name)
