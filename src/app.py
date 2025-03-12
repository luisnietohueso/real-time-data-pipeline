import streamlit as st
from data_fetcher import fetch_crypto_data, process_data

st.title("📈 Real-Time Crypto Dashboard")

data = fetch_crypto_data()
if data is not None:
    data = process_data(data)
    st.dataframe(data)
else:
    st.error("Failed to fetch data")
