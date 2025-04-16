import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("🔮 Earthquake Forecast - Next 30 Days (ML Model Output)")

# Load the predictions from your ML model
df = pd.read_csv("updated_forecast.csv")
df['date'] = pd.to_datetime(df['date'])

# Sort for display
df = df.sort_values(by='predicted_quakes', ascending=False)

# Show table
st.markdown("### 📅 Forecast Table")
st.dataframe(df)

# Show top 10 predicted high-risk events
st.markdown("### 📈 Top 10 Highest Risk Dates")
top = df.head(10)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top['country'] + " (" + top['date'].dt.strftime('%Y-%m-%d') + ")", top['predicted_quakes'], color='tomato')
ax.invert_yaxis()
ax.set_xlabel("Predicted Earthquake Count")
ax.set_title("Top Predicted Quake Events")
st.pyplot(fig)
