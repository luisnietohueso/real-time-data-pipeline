import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from data_fetcher import process_data
import pandas as pd

def test_process_data():
    data = {"id": ["bitcoin"], "symbol": ["btc"], "current_price": [50000], "market_cap": [1e12], "total_volume": [2e9]}
    df = pd.DataFrame(data)
    processed_df = process_data(df)

    assert "Market Cap (B)" in processed_df.columns
    assert "Volume (M)" in processed_df.columns
    assert processed_df["Market Cap (B)"].iloc[0] == 1000  # 1e12 / 1e9
