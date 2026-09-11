"""Main entry point for FluffFlow v2.2 with Login & Dynamic Animations."""

import random
import streamlit as st
from database import init_db, get_db
from utils import MOOD_CONFIG, CITIES, fetch_real_weather, hash_password, update_user_streak, INJECT_ANIMATED_CSS
from models import User, FluffCheckin

st.set_page_config(
    page_title="FluffFlow v2.2 — Fluffy Emotional Weather Station",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject dynamic animations & styling
st.markdown(INJECT_ANIMATED_CSS, unsafe_allow_html=True)

# Initialize clean DB
init_db()

# Session State for Authentication
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

db = next(get_db())

# --- LOGIN / REGISTRATION SYSTEM ---
if st.session_state.user_id is None:
    st.title("☕ Welcome to FluffFlow v2.2")
    st.subheader("Your daily emotional weather station powered by real weather data & fluff.")
    
    tab_login, tab_signup = st.tabs(["🔒 Login", "✨ Sign Up"])
    
    with tab_login:
        st.markdown("### Access Your Station")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", type="primary"):
            user = db.query(User).filter_by(username=login_user.strip()).first()
            if user and user.password_hash == hash_password(login_pass):
                st.session_state.user_id = user.id
                st.session_state.username = user.username
                st.success(f"Welcome back, {user.username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
                
    with tab_signup:
        st.markdown("### Create Your Account")
        signup_user = st.text_input("Choose Username", key="signup_user")
        signup_pass = st.text_input("Choose Password", type="password", key="signup_pass")
        if st.button("Create Profile", type="primary"):
            if not signup_user.strip() or not signup_pass:
                st.warning("Please fill in all fields.")
            else:
                existing = db.query(User).filter_by(username=signup_user.strip()).first()
                if existing:
                    st.error("Username already taken!")
                else:
                    new_user = User(
                        username=signup_user.strip(),
                        password_hash=hash_password(signup_pass),
                        current_streak=0
                    )
                    db.add(new_user)
                    db.commit()
                    db.refresh(new_user)
                    st.session_state.user_id = new_user.id
                    st.session_state.username = new_user.username
                    st.success("Account created successfully!")
                    st.rerun()
    st.stop()

# --- AUTHENTICATED APPLICATION INTERFACE ---
user = db.query(User).get(st.session_state.user_id)

with st.sidebar:
    st.title("☕ FluffFlow v2.2")
    st.caption("Your daily emotional weather station")
    st.divider()
    
    st.subheader(f"👤 Profile: **{user.username}**")
    st.metric(label="🔥 Current Daily Streak", value=f"{user.current_streak} Days")
    
    if st.button("🚪 Log Out"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
        
    st.divider()
    
    st.subheader("🌐 Live Weather Engine")
    selected_city = st.selectbox("Choose Location:", list(CITIES.keys()), index=0)
    weather = fetch_real_weather(selected_city)
    
    st.metric(label=f"Weather in {weather['city']}", value=f"{weather['temp']} °C", delta=weather['desc'])

# --- MAIN DASHBOARD VIEW ---
st.title("🌧️ FluffFlow: Daily Emotional Weather Station ☕")
st.markdown("### *“Tell me your vibe. I’ll serve you the perfect fluffy drink based on today’s real weather.”*")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Record Your Vibes Today")
    
    selected_mood = st.radio(
        "How is your internal weather feeling right now?",
        options=list(MOOD_CONFIG.keys()),
        index=0
    )
    
    energy_level = st.slider(
        "⚡ Energy Level (1 = Low Battery, 4 = Overcharged)",
        min_value=1,
        max_value=4,
        value=2
    )
    
    user_note = st.text_area("✍️ Add an optional fluffy thought or daily diary snippet:", placeholder="Felt like a lazy cat today...")

    btn_brew = st.button("✨ Brew My Fluffy Recommendation", type="primary", use_container_width=True)

with col2:
    st.subheader("2. Your Personalized Daily Recipe")
    
    if btn_brew:
        mood_data = MOOD_CONFIG[selected_mood]
        selected_drink = random.choice(mood_data["drinks"])
        selected_quote = random.choice(mood_data["quotes"])
        
        new_checkin = FluffCheckin(
            user_id=user.id,
            mood=selected_mood,
            energy_level=energy_level,
            weather_city=weather["city"],
            temperature=weather["temp"],
            weather_desc=weather["desc"],
            drink_name=selected_drink,
            quote=selected_quote,
            user_note=user_note
        )
        db.add(new_checkin)
        update_user_streak(db, user)
        
        st.balloons()
        st.snow()
        
        st.success("🎉 Check-in saved & streak updated!")
        
        st.markdown(
            f"""
            <div style="background-color: rgba(254, 243, 199, 0.85); padding: 25px; border-radius: 16px; border-left: 6px solid #D97706; box-shadow: 0px 8px 24px rgba(0,0,0,0.05);">
                <h3 style="color: #78350F; margin-top:0;">☕ Drink Served: {selected_drink}</h3>
                <p style="font-size: 1.15em; color: #92400E;"><b>💭 Fluffy Wisdom:</b> <i>"{selected_quote}"</i></p>
                <hr style="border: 0.5px solid #FDE68A;"/>
                <p style="margin-bottom:0; color: #78350F;"><b>🌍 Paired with real weather:</b> {weather['temp']}°C ({weather['desc']}) in {weather['city']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("👈 Select your vibe on the left and click **'Brew My Fluffy Recommendation'** to unlock your daily recipe!")
