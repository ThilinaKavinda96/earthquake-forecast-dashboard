import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 🧭 Streamlit page setup
st.set_page_config(page_title="Earthquake Forecast Map", layout="wide")

# 🌍 App title
st.title("🌍 Top 30 Earthquake Forecasts (Next 5 Years)")

# 📥 Load forecast data
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")
    df.columns = [col.strip().lower() for col in df.columns]

    # Parse date
    df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["time"])

    # Filter only future
    df = df[df["time"] >= datetime.now()]

    return df

df = load_forecast()

# ✅ Get top 30 based on predicted quake count
top30 = df.sort_values(by="predicted_quakes", ascending=False).head(30)

# 📋 Show forecast table
st.markdown("### 📅 Top 30 Forecasted Earthquakes")
st.dataframe(top30[["time", "country", "predicted_quakes", "magnitude_range"]])

# 🎨 Color by magnitude
def get_color(mag_range):
    if "Severe" in mag_range:
        return "red"
    elif "Moderate" in mag_range:
        return "orange"
    else:
        return "green"

# 🌐 Create map if coordinates available
if "latitude" in top30.columns and "longitude" in top30.columns:
    m = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in top30.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=min(max(row["predicted_quakes"], 2), 10),
            color=get_color(row["magnitude_range"]),
            fill=True,
            fill_opacity=0.8,
            popup=(
                f"<b>{row['country']}</b><br>"
                f"Date: {row['time'].strftime('%Y-%m-%d')}<br>"
                f"Magnitude: {row['magnitude_range']}<br>"
                f"Predicted Quakes: {row['predicted_quakes']:.2f}"
            )
        ).add_to(m)

    st.markdown("### 🗺️ Map of Top 30 Forecasted Earthquakes")
    st_folium(m, width=1200, height=600)
else:
    st.warning("⚠️ Latitude/Longitude columns missing from data.")
