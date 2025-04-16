import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 🧭 Configure Streamlit page
st.set_page_config(page_title="Earthquake Forecast Dashboard", layout="wide")

# 🌍 App title
st.title("🔮 Earthquake Forecast (Next 5 Years)")

# 📥 Load forecast CSV
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")

    # 🔧 Clean and standardize column names
    df.columns = [col.strip().lower() for col in df.columns]
    df.rename(columns={"predicted_": "predicted_quakes"}, inplace=True)

    # 🕒 Parse date column (dayfirst for dd/mm/yyyy format)
    df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["time"])

    # ✅ Keep only future predictions (compare with naive datetime)
    df = df[df["time"] >= datetime.now()]

    return df.sort_values(by="predicted_quakes", ascending=False)

# Load data
df = load_forecast()

# 📋 Display full table
st.markdown("### 📅 Forecasted Earthquakes (Sorted by Count)")
st.dataframe(df[["time", "country", "predicted_quakes", "magnitude_range"]])

# 📊 Show Top 10 predicted high-risk days
st.markdown("### 🌋 Top 10 Highest Risk Earthquake Days")
top = df.head(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top["country"] + " (" + top["time"].dt.strftime('%Y-%m-%d') + ")",
    top["predicted_quakes"],
    color="crimson"
)
ax.invert_yaxis()
ax.set_xlabel("Predicted Earthquake Count")
ax.set_title("Top 10 Forecasted High-Risk Days")
st.pyplot(fig)

# 📌 Footer
st.markdown("---")
st.caption("📡 ML-based Earthquake Prediction • Created by Thilina")
