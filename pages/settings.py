"""Settings Page."""

import streamlit as st
from database import get_db
from models import User

st.set_page_config(page_title="Settings — FluffFlow", page_icon="⚙️")

st.title("⚙️ Account & Station Settings")

if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please log in from the home station.")
    st.stop()

db = next(get_db())
user = db.query(User).get(st.session_state.user_id)

st.subheader(f"Account: **{user.username}**")
st.write(f"Member since: {user.created_at.strftime('%Y-%m-%d')}")
st.write(f"Active streak: {user.current_streak} Days")
