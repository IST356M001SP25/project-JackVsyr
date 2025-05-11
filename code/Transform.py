import time
import random
import csv
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import re
import pandas as pd
from Scraper import main as run_scraper

"""
Transformation script for cleaning and formatting scraped aircraft listings.

- Loads the latest scraped CSV file
- Cleans column names, normalizes prices and numeric fields
- Outputs a cleaned CSV file for visualization
"""


def ec_data():

    # --- Run the Scraper before transformation
    run_scraper()

    today_date = time.strftime("%Y%m%d")
    filename = f"ASOlistings_{today_date}.csv"

# ✅ Function to clean the CSV file to make it manipulatable for analysis
    def clean_csv(filename):
        df = pd.read_csv(filename)

        # Debugging: Print sample aircraft names before splitting
        print("Sample Aircraft Names Before Splitting:")
        print(df['Aircraft Name'].head(10))  # Print first 10 rows to check the format

        # Split into Year, Make, and Model (Simple 3-Part Split)
        df[['Year', 'Make', 'Model']] = df['Aircraft Name'].str.split(n=2, expand=True)

        # Remove the original 'Aircraft Name' column
        df.drop(columns=['Aircraft Name'], inplace=True)

        # Clean Price and TTAF columns
        df['Price'] = df['Price'].astype(str).str.replace(',', '').str.replace('$', '').str.strip()
        df['TTAF'] = df['TTAF'].astype(str).str.replace(',', '').str.strip()
        df['Landings'] = df['Landings'].astype(str).str.replace(',', '').str.strip()

        # Ensure final column order
        final_columns = ['Year', 'Make', 'Model', 'Reg #', 'Serial Number', 'Price', 'TTAF', 'Landings', 'Location', 'Company', 'URL']
        
        # Keep only the relevant columns & reorder them
        df = df[final_columns]

        # Save the cleaned CSV
        cleaned_filename = f"Cleaned_{filename}"
        df.to_csv(cleaned_filename, index=False)
        print(f"\n✅ Cleaned CSV file saved as {cleaned_filename}")

    # Call clean_csv so the transformation occurs
    clean_csv(filename)

if __name__ == "__main__":
    ec_data()