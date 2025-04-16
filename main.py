import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🔮 Earthquake Magnitude Classifier (Next 30 Days)")

# Load the predictions from your model output
df = pd.read_csv("updated_forecast.csv")
df['time'] = pd.to_datetime(df['time'])

# Sort by highest magnitude
df_sorted = df.sort_values(by='mag', ascending=False)

# Show table
st.markdown("### 📊 Earthquake Predictions (Sorted by Magnitude)")
st.dataframe(df_sorted[['time', 'country', 'latitude', 'longitude', 'depth', 'mag', 'mag_class']])

# Plot top 10 high-magnitude forecasts
top_10 = df_sorted.head(10)

st.markdown("### 🌋 Top 10 Highest Magnitude Earthquakes")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_10['country'] + " (" + top_10['time'].dt.strftime('%Y-%m-%d') + ")",
        top_10['mag'],
        color='darkred')
ax.invert_yaxis()
ax.set_xlabel("Magnitude")
st.pyplot(fig)
