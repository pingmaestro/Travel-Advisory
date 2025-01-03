#!/usr/bin/env python
# coding: utf-8

# In[59]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://travel.gc.ca/travelling/advisories"
response = requests.get(url)

if response.status_code == 200:
    print("Page fetched successfully!")

    soup = BeautifulSoup(response.content, "html.parser")

    page_title = soup.title.text
    print(f"Page title: {page_title}")

    advisory_rows = soup.find_all("tr")
    
    advisories = []
    
    # Loop through each row and extract relevant columns
    for row in advisory_rows:
        columns = row.find_all("td")
        
        if len(columns) >= 4:
            destination = columns[1].find("a").text.strip() 

            anchor_tag = columns[1].find("a")
            if anchor_tag and "href" in anchor_tag.attrs:
                slug_url = anchor_tag["href"].strip()
            else:
                slug_url = ""
            
            risk_level = columns[2].find("div").text.strip()
            last_updated = columns[3].text.strip()
        
            advisories.append({
                "Destination": destination,
                "URL": slug_url,
                "Risk Level": risk_level,
                "Last Updated": last_updated
            })

    df = pd.DataFrame(advisories)

    df.to_csv("travel_advisories.csv", index=False, encoding="utf-8-sig")

    print("Data exported to 'travel_advisories.csv' successfully.")
else:
    print(f"Failed to retrieve the page. Status code : {response.status_code}")

