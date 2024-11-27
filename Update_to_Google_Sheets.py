#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import gspread
import requests
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Travel Advisories Data - Canada").sheet1

url = "https://raw.githubusercontent.com/pingmaestro/Travel-Advisory/main/travel_advisories.csv"
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(url)

    sheet.clear()

    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("Google Sheet updated successfully.")
else:
    print("Failed to fetch CSV from GitHub.")

