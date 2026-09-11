"""Fluff Vault Page — Displays user history with real-time Plotly mood chart."""

import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_db
from models import FluffCheckin, User

st.set_page_config(page_title="Fluff Vault — FluffFlow", page_icon="📦")

st.title("📦 Fluff Vault & Mood Timeline")

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in from the home station to view your vault.")
    st.stop()

db = next(get_db())
user = db.query(User).get(st.session_state.user_id)
checkins = db.query(FluffCheckin).filter_by(user_id=user.id).order_by(FluffCheckin.timestamp.asc()).all()

if not checkins:
    st.info("📜 Your Fluff Vault is completely clean. Go to the Home station to record your first real check-in!")
else:
    data = []
    for c in checkins:
        data.append({
            "Date": c.checkin_date.strftime("%Y-%m-%d"),
            "Mood": c.mood,
            "Energy Level": c.energy_level,
            "Temperature (°C)": c.temperature,
            "Weather": c.weather_desc,
            "Drink Recommendation": c.drink_name,
            "Fluffy Quote": c.quote,
            "Personal Note": c.user_note or "-"
        })
    
    df = pd.DataFrame(data)
    
    st.subheader("📈 Your Weather vs Energy Trends")
    fig = px.line(df, x="Date", y="Temperature (°C)", markers=True, title="Temperature vs Log Date", color_discrete_sequence=["#D97706"])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📜 Check-In Vault History")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
