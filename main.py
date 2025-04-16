import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 🔧 Setup Streamlit
st.set_page_config(page_title="Earthquake Forecast Dashboard", layout="wide")
st.title("🌍 Earthquake Forecast - 5 Year Prediction")

# 📥 Load and preprocess forecast data
@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")
    df.columns = [col.strip().lower() for col in df.columns]

    df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["time"])
    df = df[df["time"] >= datetime.now()]

    return df.sort_values(by="time", ascending=True)

df = load_forecast()

# 📋 Show FULL 5-Year Forecast Table
st.markdown("### 📅 All Earthquake Forecasts (Next 5 Years, Chronological)")
st.dataframe(df[["time", "country", "predicted_quakes", "magnitude_range"]])

# 🎯 Take FIRST 30 ROWS from the table (for mapping)
top30 = df.head(30)

# 🎨 Marker color by magnitude
def get_color(mag_range):
    if "Severe" in mag_range:
        return "red"
    elif "Moderate" in mag_range:
        return "orange"
    else:
        return "green"

# 🗺️ Create Folium map
if "latitude" in top30.columns and "longitude" in top30.columns:
    st.markdown("### 🗺️ Map of First 30 Upcoming Earthquake Forecasts")

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

    st_folium(m, width=1200, height=600)
else:
    st.warning("⚠️ Latitude and longitude columns are missing.")
