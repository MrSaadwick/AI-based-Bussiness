pip install seaborn
pip install matplotlib

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

import openai

openai.api_key = "YOUR_API_KEY"

def get_ai_advice(data_summary):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a business analyst. Provide 3 actionable strategies based on this data:"},
            {"role": "user", "content": str(data_summary)}
        ]
    )
    return response.choices[0].message['content']

# In your Streamlit app:
if st.button("🤖 Get AI Recommendations"):
    summary = f"Top products: {top_products.index.tolist()}. Total profit: ${total_profit:,.2f}"
    advice = get_ai_advice(summary)
    st.write(advice)

from prophet import Prophet

# Prepare data
forecast_df = df.groupby('Order Date')['Total Revenue'].sum().reset_index()
forecast_df.columns = ['ds', 'y']

# Train model
model = Prophet()
model.fit(forecast_df)

# Predict next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Show forecast
st.subheader("📈 Revenue Forecast")
st.line_chart(forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']])
