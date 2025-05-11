import os
import pandas as pd
from datetime import datetime
from code.Transform import ec_data as transform_data
from code.Scraper import scrape_listings

def test_scraper_output():
    """Test that the scraper creates a CSV file with today's date in the name."""
    today = datetime.today().strftime('%Y%m%d')
    expected_filename = f"ASOlistings_{today}.csv"
    assert os.path.exists(expected_filename), f"{expected_filename} was not created by the scraper."

def test_transform_output():
    """Test that the transform function returns a DataFrame and is not empty."""
    df = transform_data()
    assert isinstance(df, pd.DataFrame), "Output is not a DataFrame."
    assert not df.empty, "Transformed DataFrame is empty."

if __name__ == "__main__":
    test_scraper_output()
    test_transform_output()
    print("All tests passed.")