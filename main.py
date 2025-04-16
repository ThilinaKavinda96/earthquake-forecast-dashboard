import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("🔮 Earthquake Magnitude Classifier (Next 30 Days)")

# Load and parse time safely
df = pd.read_csv("updated_forecast.csv")
df['time'] = pd.to_datetime(df['time'], errors='coerce', utc=True)

# Optional: only keep future events
df = df[df['time'] > datetime.utcnow()]
df = df.dropna(subset=['time'])

# Sort by magnitude
df_sorted = df.sort_values(by='mag', ascending=False)

# Show table
st.markdown("### 📊 Earthquake Predictions (Sorted by Magnitude)")
st.dataframe(df_sorted[['time', 'country', 'latitude', 'longitude', 'depth', 'mag', 'mag_class']])

# Plot top 10
top_10 = df_sorted.head(10)
st.markdown("### 🌋 Top 10 Highest Magnitude Earthquakes")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_10['country'] + " (" + top_10['time'].dt.strftime('%Y-%m-%d') + ")",
        top_10['mag'],
        color='darkred')
ax.invert_yaxis()
ax.set_xlabel("Magnitude")
st.pyplot(fig)
