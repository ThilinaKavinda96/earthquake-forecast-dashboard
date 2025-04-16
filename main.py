import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone

st.set_page_config(page_title="Earthquake Forecast Dashboard", layout="wide")

# Load future forecasts
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")
    df['time'] = pd.to_datetime(df['time'], errors='coerce', utc=True)
    df = df.dropna(subset=['time'])

    # ✅ Fix: compare timezone-aware datetimes
    df = df[df['time'] >= datetime.now(timezone.utc)]
    return df.sort_values(by="predicted_quakes", ascending=False)

df = load_forecast()

# Title
st.title("🔮 Earthquake Forecast (Next 30 Days)")

# Show forecast table
st.markdown("### 📅 Forecasted Earthquake Events")
st.dataframe(df[['time', 'country', 'predicted_quakes', 'magnitude_range']])

# Plot Top 10
st.markdown("### 🌋 Top 10 Highest Predicted Earthquake Days")
top = df.head(10)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top['country'] + " (" + top['time'].dt.strftime('%Y-%m-%d') + ")",
    top['predicted_quakes'],
    color='orange'
)
ax.invert_yaxis()
ax.set_xlabel("Predicted Earthquake Count")
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("📡 Live model predictions powered by ML • Created by Chathura")
