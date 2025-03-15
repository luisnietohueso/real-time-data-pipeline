import sys
import os
import pandas as pd

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from data_fetcher import process_data

def test_process_data():
    # Simulated API response (list of dictionaries)
    data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "current_price": 50000,
            "market_cap": 1e12,  # 1 Trillion
            "total_volume": 2e9   # 2 Billion
        }
    ]

    processed_df = process_data(data)

    # Ensure column renaming and conversions are correct
    assert "Market Cap (B)" in processed_df.columns
    assert "Volume (M)" in processed_df.columns
    assert processed_df["Market Cap (B)"].iloc[0] == 1000  # 1e12 / 1e9
    assert processed_df["Volume (M)"].iloc[0] == 2000  # 2e9 / 1e6

    print("Test `test_process_data()` passed!")

# Run the test manually if executing this script directly
if __name__ == "__main__":
    test_process_data()
