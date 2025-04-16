import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 🧭 Configure page
st.set_page_config(page_title="Earthquake Forecast Dashboard", layout="wide")

# 🌍 Title
st.title("🔮 Earthquake Forecast (Next 5 Years)")

# 📥 Load forecast data
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")

    # Clean column names
    df.columns = [col.strip().lower() for col in df.columns]
    df.rename(columns={"predicted_": "predicted_quakes"}, inplace=True)

    # Parse date column
    df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["time"])

    # ✅ Filter only future predictions
    df = df[df["time"] >= datetime.now()]

    # ✅ Sort table by upcoming date
    return df.sort_values(by="time", ascending=True)

df = load_forecast()

# 📋 Display Table (sorted by time)
st.markdown("### 📅 Forecasted Earthquakes (Soonest First)")
st.dataframe(df[["time", "country", "predicted_quakes", "magnitude_range"]])

# 📊 Top 10 High-Risk Days (sorted by quake count)
st.markdown("### 🌋 Top 10 Highest Predicted Earthquake Days")
top = df.sort_values(by="predicted_quakes", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top["country"] + " (" + top["time"].dt.strftime('%Y-%m-%d') + ")",
    top["predicted_quakes"],
    color="crimson"
)
ax.invert_yaxis()
ax.set_xlabel("Predicted Earthquake Count")
ax.set_title("Top 10 High-Risk Days by Earthquake Activity")
st.pyplot(fig)

# 📌 Footer
st.markdown("---")
st.caption("📡 ML-based Earthquake Forecast • Powered by Prophet • Created by Thilina")
