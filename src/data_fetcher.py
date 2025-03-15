import requests
import pandas as pd

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error if request fails
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            print("API response received:", data[:3])  # Print first 3 entries for debugging
            return data
        else:
            print("API returned an empty response.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
        return None
    
def process_data(data):
    if isinstance(data, list):  # Ensure data is a list before conversion
        df = pd.DataFrame(data)  # Convert list of dictionaries to DataFrame
    else:
        raise ValueError(f"Expected a list of dictionaries, but got: {type(data)}")

    # ✅ Ensure "id" is preserved
    required_columns = ["id", "symbol", "market_cap", "total_volume", "current_price"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Missing expected column: {col}")

    # Convert market cap to billions, volume to millions
    df["market_cap"] = df["market_cap"] / 1e9  # Convert to billion
    df["total_volume"] = df["total_volume"] / 1e6  # Convert to million

    # Rename columns for better readability
    df.rename(columns={"market_cap": "Market Cap (B)", "total_volume": "Volume (M)"}, inplace=True)

    return df

if __name__ == "__main__":
    raw_data = fetch_crypto_data()
    if raw_data is not None:
        processed_data = process_data(raw_data)
        print(processed_data)
