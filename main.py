import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Earthquake Forecast", layout="wide")

# App Title
st.title("🌍 Earthquake Magnitude Classifier")

# 📥 Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("updated_forecast.csv")
    df['time'] = pd.to_datetime(df['time'], errors='coerce', utc=True)
    df = df.dropna(subset=['time'])
    return df

df = load_data()

# Optional: Filter by recent years only (you can tweak this)
# df = df[df['time'].dt.year >= 2020]

# 🧮 Sort by magnitude
df_sorted = df.sort_values(by='mag', ascending=False)

# 📊 Show Table
st.markdown("### 📋 Earthquake Predictions")
st.dataframe(df_sorted[['time', 'country', 'latitude', 'longitude', 'depth', 'mag', 'mag_class']])

# 🌋 Top 10 Magnitude Events
top_10 = df_sorted.head(10)

st.markdown("### 🔥 Top 10 Highest Magnitude Earthquakes")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(
    top_10['country'] + " (" + top_10['time'].dt.strftime('%Y-%m-%d') + ")",
    top_10['mag'],
    color='crimson'
)
ax.invert_yaxis()
ax.set_xlabel("Magnitude")
ax.set_title("Top 10 Predicted Earthquakes by Magnitude")
st.pyplot(fig)

# 📌 Footer
st.markdown("---")
st.caption("Created by Thilina • Earthquake Forecasting using Machine Learning 🌐")
