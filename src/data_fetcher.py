import requests
import pandas as pd

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 5, "page": 1}

def fetch_crypto_data():
    response = requests.get(API_URL, params=PARAMS)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)[["id", "symbol", "current_price", "market_cap", "total_volume"]]
        return df
    else:
        print("Error fetching data")
        return None
    
def process_data(df):
    df["market_cap"] = df["market_cap"] / 1e9  # Convert to billion
    df["total_volume"] = df["total_volume"] / 1e6  # Convert to million
    df.rename(columns={"market_cap": "Market Cap (B)", "total_volume": "Volume (M)"}, inplace=True)
    return df

if __name__ == "__main__":
    df = fetch_crypto_data()
    if df is not None:
        df = process_data(df)
        print(df)
