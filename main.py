import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Earthquake Forecast Map", layout="wide")
st.title("🌍 Earthquake Forecast (Next 5 Years) - Map View")

@st.cache_data
def load_forecast():
    df = pd.read_csv("updated_forecast.csv")
    df.columns = [col.strip().lower() for col in df.columns]
    df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["time"])
    df = df[df["time"] >= datetime.now()]
    return df.sort_values(by="time", ascending=True)

df = load_forecast()

st.markdown("### 📅 Forecasted Earthquakes")
st.dataframe(df[["time", "country", "predicted_quakes", "magnitude_range"]])

def get_color(mag_range):
    if "Severe" in mag_range:
        return "red"
    elif "Moderate" in mag_range:
        return "orange"
    else:
        return "green"

if "latitude" in df.columns and "longitude" in df.columns:
    m = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=min(max(row["predicted_quakes"], 2), 10),
            color=get_color(row["magnitude_range"]),
            fill=True,
            fill_opacity=0.7,
            popup=f"""
                <b>{row['country']}</b><br>
                Date: {row['time'].strftime('%Y-%m-%d')}<br>
                Magnitude: {row['magnitude_range']}<br>
                Forecasted Quakes: {row['predicted_quakes']:.2f}
            """
        ).add_to(m)

    st.markdown("### 🗺️ Global Forecast Map")
    st_folium(m, width=1200, height=600)
else:
    st.warning("Coordinates not found in the data. Please include latitude and longitude.")
