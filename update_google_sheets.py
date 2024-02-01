# update_google_sheets.py
from __future__ import print_function
import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import time
from tqdm import tqdm
import pandas as pd

def get_credentials():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    path = (os.path.join(os.getcwd(), 'creds.json'))
    creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
    return creds

def update_google_sheet(sheet_id, csv_filename):
    creds = get_credentials()
    client = gspread.authorize(creds)

    # Load the data from the CSV file
    df = pd.read_csv(csv_filename)

    sheet_id = '1sBebAgcrHDLXWse8vo2xqtHaHOblSjm1aLWyd8HKY2U'
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1

    # Write the headers to the sheet
    headers = df.columns.tolist()
    worksheet.update_row(1, headers)

    # Write the data to the sheet
    for index, row in tqdm(df.iterrows(), desc="Updating Google Sheet"):
        time.sleep(1)
        row_data = row.tolist()
        worksheet.update_row(index + 2, row_data)

# Example usage
csv_filename = 'data020124-1651.csv'  # Replace with your actual CSV filename
sheet_id = '1sBebAgcrHDLXWse8vo2xqtHaHOblSjm1aLWyd8HKY2U'
update_google_sheet(sheet_id, csv_filename)
