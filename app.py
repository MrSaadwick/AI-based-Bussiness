import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 AI Business Intelligence Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload your sales data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Show Data
    if st.checkbox("Show raw data"):
        st.dataframe(df)

    # Analysis
    st.header("🔍 Insights")
    
    # Top Products
    st.subheader("Top 5 Profitable Products")
    top_products = df.groupby("Item Type")["Total Profit"].sum().nlargest(5)
    st.bar_chart(top_products)

    # Sales Channel Performance
    st.subheader("Sales Channel Performance")
    channel_profit = df.groupby("Sales Channel")["Total Profit"].sum()
    st.pie_chart(channel_profit)

    # Download Report Button
    if st.button("📥 Generate Full Report"):
        st.success("Report generated! (This would trigger your PDF code)")