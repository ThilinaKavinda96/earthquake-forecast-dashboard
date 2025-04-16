import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone

st.set_page_config(page_title="Earthquake Forecast Dashboard", layout="wide")

# 🌍 App Title
st.title("🔮 Earthquake Forecast (Next 5 Years)")

# 📥 Load data
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")

    # 🛠 Clean and parse columns
    df.columns = [col.strip().lower() for col in df.columns]
    df.rename(columns={"predicted_": "predicted_quakes"}, inplace=True)

    # 🕒 Parse time safely
    df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["time"])

    # ✅ Keep only future predictions
    df = df[df["time"] >= datetime.now(timezone.utc)]

    return df.sort_values(by="predicted_quakes", ascending=False)

df = load_forecast()

# 📋 Forecast Table
st.markdown("### 📅 Forecasted Earthquakes")
st.dataframe(df[["time", "country", "predicted_quakes", "magnitude_range"]])

# 📊 Top 10 High Risk Days
st.markdown("### 🌋 Top 10 Highest Predicted Earthquake Days")
top = df.head(10)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top["country"] + " (" + top["time"].dt.strftime('%Y-%m-%d') + ")",
    top["predicted_quakes"],
    color="crimson"
)
ax.invert_yaxis()
ax.set_xlabel("Predicted Earthquake Count")
ax.set_title("Top 10 High Risk Days (By Earthquake Frequency)")
st.pyplot(fig)

# 📌 Footer
st.markdown("---")
st.caption("📡 Powered by ML + Prophet • Created by Thilina")
