#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import gspread
import requests
import pandas as pd
import json  # Importing json to handle JSON operations
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Set up credentials for Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Create a credentials object from the credentials.json file
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Step 2: Get the Google Sheet
sheet = client.open("Travel Advisories Data").sheet1

# Step 3: Fetch the latest CSV from GitHub
url = "https://raw.githubusercontent.com/pingmaestro/Travel-Advisory/main/travel_advisories.csv"
response = requests.get(url)

# Step 4: Read the CSV into a DataFrame
if response.status_code == 200:
    df = pd.read_csv(url)

    # Step 5: Clear existing Google Sheet data
    sheet.clear()

    # Step 6: Update Google Sheet with new data
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("Google Sheet updated successfully.")
else:
    print("Failed to fetch CSV from GitHub.")