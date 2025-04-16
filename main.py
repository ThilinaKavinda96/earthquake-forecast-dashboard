import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Earthquake Forecast Dashboard", layout="wide")

# Load the model's forecast file
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time'])

    # 🟢 Only show future predictions
    df = df[df['time'] >= datetime.now()]
    return df.sort_values(by="predicted_quakes", ascending=False)

df = load_forecast()

# Title
st.title("🔮 Earthquake Forecast for Next 30 Days")

# Display forecast table
st.markdown("### 📅 Predicted Earthquake Events")
st.dataframe(df[['time', 'country', 'predicted_quakes', 'magnitude_range']])

# Chart - Top 10 predicted high quake dates
st.markdown("### 📈 Top Predicted Risk Dates")
top = df.head(10)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top['country'] + " (" + top['time'].dt.strftime('%Y-%m-%d') + ")",
    top['predicted_quakes'],
    color='orangered'
)
ax.invert_yaxis()
ax.set_xlabel("Predicted Earthquake Count")
st.pyplot(fig)

st.markdown("---")
st.caption("Powered by ML & Prophet • Forecasting earthquakes up to 30 days ahead.")
