import requests 
import pandas as pd
from bs4 import BeautifulSoup
import re

# Wikipedia URL (List of countries by GDP)
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all tables with class "wikitable"
tables = soup.find_all("table", {"class": "wikitable"})

# Loop through all tables and extract data
all_dataframes = []
for i, table in enumerate(tables):
    # Extract table headers
    headers = [header.text.strip() for header in table.find_all("th")]

    # Extract table rows
    rows = []
    for row in table.find_all("tr")[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) > 0:
            row_data = [cell.text.strip() for cell in cells]
            rows.append(row_data)

    # Save to Pandas DataFrame
    df = pd.DataFrame(rows, columns=headers[:len(rows[0])])  # Match columns

    # ✅ Remove footnotes like [n 1], [n 2], etc.
    df = df.replace(r"\[\w* \d+\]", "", regex=True)

    # ✅ Remove any remaining square brackets and extra spaces
    df = df.replace(r"\[.*?\]", "", regex=True)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # ✅ Remove unwanted characters (e.g., $, commas, newlines)
    df = df.replace(r"[\$,]", "", regex=True)
    df = df.replace(r"\s+", " ", regex=True)  # Replace multiple spaces with a single space
    
    # ✅ Convert numerical columns to numeric values
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')  # Ignore errors for non-numeric columns

    # ✅ Store DataFrame
    all_dataframes.append(df)

    # ✅ Save each table as CSV
    filename = f"wikipedia_table_{i+1}.csv"
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved: {filename}")

    # ✅ Print table info
    print(f"\n--- Table {i+1} ---")
    print(df.head())  # Show first 5 rows of each table

# ✅ Merge all tables into one CSV if needed
merged_df = pd.concat(all_dataframes, ignore_index=True)
merged_df.to_csv("task_2_all_tables.csv", index=False, encoding="utf-8")
print("\n✅ All tables combined and saved as 'wikipedia_all_tables.csv'")
