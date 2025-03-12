import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from data_fetcher import fetch_crypto_data, process_data

# Set Streamlit Page Config
st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("Real-Time Cryptocurrency Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
num_coins = st.sidebar.slider("Number of Cryptos to Display", 1, 50, 10)
sort_by = st.sidebar.selectbox("Sort by", ["Market Cap", "Price", "Volume"])
sort_column_map = {
    "Market Cap": "Market Cap (B)",
    "Price": "current_price",
    "Volume": "Volume (M)"
}

# Fetch and Process Data
data = fetch_crypto_data()
if data is not None:
    data = process_data(data)
    
    # Sort and Filter Data
    data = data.sort_values(by=sort_column_map[sort_by], ascending=False).head(num_coins)

    # Display Market Data Table
    st.subheader("Market Data")
    st.dataframe(data)

    # Bar Chart: Price Comparison
    st.subheader("Price Comparison")
    price_chart = alt.Chart(data).mark_bar().encode(
        x="symbol",
        y="current_price",
        color="symbol",
        tooltip=["id", "symbol", "current_price"]
    ).interactive()
    st.altair_chart(price_chart, use_container_width=True)


else:
    st.error("Failed to fetch data. Please try again later.")

top_n = 10  # Show only the top 10 coins, the rest will be grouped as "Others"
if len(data) > top_n:
    others = data.iloc[top_n:].sum(numeric_only=True)  # Sum market cap of remaining coins
    data = data.iloc[:top_n]  # Keep only top N coins
    data = pd.concat([data, pd.DataFrame([{"symbol": "Others", "Market Cap (B)": others["Market Cap (B)"]}])], ignore_index=True)

# Create Pie Chart
st.subheader("Market Cap Share")

fig, ax = plt.subplots(figsize=(9, 7))  # Increased figure size for better readability
explode = [0.1] + [0] * (len(data) - 1)  # Highlight the largest segment (Bitcoin)

# Define colors with a colormap
colors = plt.get_cmap("tab10")(range(len(data)))

# Plot the pie chart
wedges, texts, autotexts = ax.pie(
    data["Market Cap (B)"],
    labels=data["symbol"],
    autopct=lambda p: f"{p:.1f}%" if p > 2 else "",  # Show % only if >2% to reduce clutter
    startangle=140,
    pctdistance=0.85,
    explode=explode,
    colors=colors,
    wedgeprops={"edgecolor": "white", "linewidth": 1}
)

# Improve label readability by adding a bounding box
for text in texts:
    text.set_fontsize(10)
    text.set_bbox(dict(facecolor="white", alpha=0.7, edgecolor="none"))

# Make percentage labels bold
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_color("black")
    autotext.set_fontweight("bold")

# Draw a circle at the center to make it look like a donut
centre_circle = plt.Circle((0, 0), 0.70, fc="white")
fig.gca().add_artist(centre_circle)

# Set title
ax.set_title("Top Crypto Market Cap Share", fontsize=16, fontweight="bold")

# Display improved pie chart
st.pyplot(fig)