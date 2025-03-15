import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import requests
import time

from data_fetcher import fetch_crypto_data, process_data  # Ensure these functions are working

# ---- Streamlit Page Config ----
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("Real-Time Cryptocurrency Dashboard")

# ---- Sidebar Controls ----
st.sidebar.header("Dashboard Settings")
refresh_data = st.sidebar.button("Refresh Data")

num_coins = st.sidebar.slider("Number of Cryptos to Display", 1, 50, 10)
top_n = st.sidebar.slider("Number of Cryptos in Pie Chart", 5, 20, 10)
sort_by = st.sidebar.selectbox("Sort by", ["Market Cap", "Price", "Volume"])
show_table = st.sidebar.checkbox("Show Market Data Table", True)
show_bar_chart = st.sidebar.checkbox("Show Price Comparison Bar Chart", True)
show_pie_chart = st.sidebar.checkbox("Show Market Cap Pie Chart", True)
show_time_series = st.sidebar.checkbox("Show Price Trend Chart", True)

# ---- Column Mapping ----
sort_column_map = {
    "Market Cap": "Market Cap (B)",
    "Price": "current_price",
    "Volume": "Volume (M)"
}

# ---- Fetch & Process Data ----
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_crypto_data():
    """Fetch crypto data and process it."""
    raw_data = fetch_crypto_data()
    if raw_data is None:
        return None
    return process_data(raw_data)

if refresh_data or "crypto_data" not in st.session_state:
    st.session_state["crypto_data"] = get_crypto_data()

data = st.session_state["crypto_data"]

# ---- Validate Data ----
if data is None or data.empty:
    st.error("Failed to fetch cryptocurrency data. Please try again later.")
    st.stop()

# Ensure required columns exist
required_columns = ["id", "symbol", "current_price", "Market Cap (B)", "Volume (M)"]
if not all(col in data.columns for col in required_columns):
    st.error("Missing required columns in the data. Please check API response.")
    st.stop()

# ---- Sort & Filter Data ----
data = data.sort_values(by=sort_column_map[sort_by], ascending=False).head(num_coins)

# ---- Market Data Table ----
if show_table:
    st.subheader("Market Data")
    search_query = st.text_input("Search Cryptocurrency", "")
    filtered_data = data[data["symbol"].str.contains(search_query, case=False, na=False)] if search_query else data
    st.dataframe(filtered_data)

# ---- Price Comparison Bar Chart ----
if show_bar_chart:
    st.subheader("Price Comparison")
    price_chart = alt.Chart(data).mark_bar().encode(
        x="symbol",
        y="current_price",
        color="symbol",
        tooltip=["symbol", "current_price"]
    ).interactive()
    st.altair_chart(price_chart, use_container_width=True)

# ---- Market Cap Pie Chart ----
if show_pie_chart:
    st.subheader("Market Cap Share (Interactive)")

    if len(data) > top_n:
        others = data.iloc[top_n:].sum(numeric_only=True)
        data = data.iloc[:top_n]
        data = pd.concat([data, pd.DataFrame([{"symbol": "Others", "Market Cap (B)": others["Market Cap (B)"]}])], ignore_index=True)

    fig = px.pie(
        data, 
        values="Market Cap (B)", 
        names="symbol", 
        title="Top Crypto Market Cap Share",
        hover_data=["Market Cap (B)"], 
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    fig.update_traces(textinfo="percent+label", pull=[0.1 if i == 0 else 0 for i in range(len(data))])
    st.plotly_chart(fig, use_container_width=True)


# ---- Optimized Historical Data Fetching ----
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_historical_data(crypto_id, days=30):
    """
    Fetch historical price data with rate limit handling.
    Implements exponential backoff to prevent 429 errors.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 429:
                wait_time = 20 * (attempt + 1)
                print(f"Rate limit hit! Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue  # Retry

            response.raise_for_status()
            data = response.json()

            if "prices" in data:
                df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                return df

            return pd.DataFrame()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical data: {e}")
            time.sleep(5)  # Wait before retrying

    return pd.DataFrame()  # Return empty if all retries fail


# ---- Price Trend Over Time ----
if show_time_series:
    st.subheader("Price Trend Over Time")
    
    crypto_selection = st.selectbox("Select Cryptocurrency", data["symbol"])
    selected_coin_id = data.loc[data["symbol"] == crypto_selection, "id"].values[0]

    # Dynamic Date Range Selection
    days_range = st.slider("Select Data Range (Days)", 7, 365, 30)

    # Fetch and Display Historical Data
    if st.button("Load Historical Data"):
        historical_data = fetch_historical_data(selected_coin_id, days_range)

        if not historical_data.empty:
            fig = px.line(
                historical_data, 
                x="timestamp", 
                y="price", 
                title=f"{crypto_selection} Price Trend",
                labels={"timestamp": "Date", "price": "Price (USD)"},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No historical data available for {crypto_selection}.")
