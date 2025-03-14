import streamlit as st
import pandas as pd
import altair as alt
import numpy as np  
import plotly.express as px
from data_fetcher import fetch_crypto_data, process_data

# Set Streamlit Page Config
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# App Title
st.title("Real-Time Cryptocurrency Dashboard")

# Sidebar Controls
st.sidebar.header("Dashboard Settings")
refresh_data = st.sidebar.button("Refresh Data")

num_coins = st.sidebar.slider("Number of Cryptos to Display", 1, 50, 10)
top_n = st.sidebar.slider("Number of Top Cryptos in Pie Chart", 5, 20, 10)
sort_by = st.sidebar.selectbox("Sort by", ["Market Cap", "Price", "Volume"])
color_theme = st.sidebar.selectbox("Color Theme", ["Set3", "coolwarm", "viridis", "plotly"])
show_table = st.sidebar.checkbox("Show Market Data Table", True)
show_bar_chart = st.sidebar.checkbox("Show Price Comparison Bar Chart", True)
show_pie_chart = st.sidebar.checkbox("Show Market Cap Pie Chart", True)
show_time_series = st.sidebar.checkbox("Show Price Trend Chart", True)

# Column Mapping for Sorting
sort_column_map = {
    "Market Cap": "Market Cap (B)",
    "Price": "current_price",
    "Volume": "Volume (M)"
}

# Fetch and Process Data
if refresh_data or "data" not in st.session_state:
    data = fetch_crypto_data()
    if data is None:
        st.error("Failed to fetch cryptocurrency data. Please try again later.")
        st.stop()
    data = process_data(data)
    st.session_state["data"] = data  # Store in session state for persistence

data = st.session_state["data"]
data = data.sort_values(by=sort_column_map[sort_by], ascending=False).head(num_coins)

# Market Data Table
if show_table:
    st.subheader("Market Data")
    search_query = st.text_input("Search Cryptocurrency", "")
    filtered_data = data[data["symbol"].str.contains(search_query, case=False, na=False)] if search_query else data
    st.dataframe(filtered_data)

# Price Comparison Bar Chart
if show_bar_chart:
    st.subheader("Price Comparison")
    price_chart = alt.Chart(data).mark_bar().encode(
        x="symbol",
        y="current_price",
        color="symbol",
        tooltip=["id", "symbol", "current_price"]
    ).interactive()
    st.altair_chart(price_chart, use_container_width=True)

# Market Cap Pie Chart (Interactive)
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
        hole=0.4  # Donut effect
    )

    fig.update_traces(
        textinfo="percent+label",
        pull=[0.1 if i == 0 else 0 for i in range(len(data))]  # Highlight top segment
    )

    st.plotly_chart(fig, use_container_width=True)

# Time Series Price Chart
if show_time_series:
    st.subheader("Price Trend Over Time")
    selected_coin = st.selectbox("Select Cryptocurrency for Time Series", data["symbol"])
    coin_data = fetch_crypto_data()  # Simulating a time series API call
    if coin_data is not None and selected_coin in coin_data["symbol"].values:
        coin_df = coin_data[coin_data["symbol"] == selected_coin]
        fig = px.line(
            coin_df, 
            x=coin_df.index, 
            y="current_price", 
            title=f"Price Trend for {selected_coin}",
            labels={"x": "Time", "y": "Price"},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No time series data available for this cryptocurrency.")
