"""Leaderboard Page — Shows real dynamic streaks."""

import streamlit as st
import pandas as pd
from database import get_db
from models import User

st.set_page_config(page_title="Leaderboard — FluffFlow", page_icon="🏆")

st.title("🏆 FluffFlow Real Streak Leaderboard")

db = next(get_db())
users = db.query(User).filter(User.current_streak > 0).order_by(User.current_streak.desc()).limit(10).all()

if not users:
    st.info("No active user streaks recorded yet! Be the first to check in on the home page.")
else:
    leaderboard_data = []
    for idx, u in enumerate(users, start=1):
        leaderboard_data.append({
            "Rank": f"#{idx}" if idx > 3 else ["🥇", "🥈", "🥉"][idx - 1],
            "Username": u.username,
            "Current Streak": f"{u.current_streak} Days 🔥",
            "Last Check-In": str(u.last_checkin_date) if u.last_checkin_date else "Never"
        })
    
    df = pd.DataFrame(leaderboard_data)
    st.table(df)
