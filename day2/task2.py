import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page containing Java version history
URL = "https://en.wikipedia.org/wiki/Java_version_history"

# Send a request to fetch the page content
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Find all tables on the page
tables = soup.find_all("table", {"class": "wikitable"})

# List to store DataFrames
dfs = []

# Process each table
for table in tables:
    headers = [header.text.strip() for header in table.find_all("th")]  # Extract headers
    rows = table.find_all("tr")[1:]  # Skip header row

    data = []
    for row in rows:
        cols = row.find_all("td")
        row_data = [col.text.strip() for col in cols]  # Extract row data
        if row_data:  # Avoid empty rows
            data.append(row_data)

    # Convert to DataFrame and append to list
    df = pd.DataFrame(data, columns=headers[:len(data[0])])  # Ensure columns match data
    dfs.append(df)

# Combine all tables into a single CSV file
combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv("java_version_history.csv", index=False, encoding="utf-8")

print("Scraping completed! Data saved to java_version_history.csv")
