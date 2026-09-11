"""Helper functions, password hashing, weather API, and custom CSS animations."""

import requests
import hashlib
import logging
from datetime import date, timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
from models import User

logger = logging.getLogger("FluffFlowUtils")

MOOD_CONFIG: Dict[str, Dict[str, Any]] = {
    "Fluffy Sunshine ☀️": {
        "drinks": ["Vanilla Cloud Caramel Latte 🍮", "Honey Golden Oat Milk Cappuccino 🍯", "Sunburst Citrus Espresso Tonic 🍊"],
        "quotes": [
            "Your vibes are so bright, even the coffee bean wants to glow today!",
            "Radiating pure warmth! You're basically a cup of hot chocolate on a chilly day.",
            "Shine on! The world is your oversized fluffy blanket right now."
        ]
    },
    "Mild Chaos 🌀": {
        "drinks": ["Iced Dirty Chai with Extra Cinnamon ☕", "Sparkling Matcha Lemonade 🍋", "Double Espresso over Salted Caramel Ice 🧊"],
        "quotes": [
            "Embrace the swirl! A little chaos just means life is frothing correctly.",
            "You aren't messy, you're an artisanal limited-edition cold brew process.",
            "Spinning around with purpose. Drink up and steer the hurricane!"
        ]
    },
    "Stormy Existential 🌩️": {
        "drinks": ["Deep Mocha Dark Chocolate Drizzle 🍫", "Smoky Cardamom Warm Milk 🌌", "Midnight Charcoal French Press ☕"],
        "quotes": [
            "It's okay to sit in the rain sometimes. Just make sure your coffee stays warm.",
            "The clouds will pass, but this deep velvety comfort is right here with you.",
            "Contemplating the cosmos is thirsty work. Sip slowly and breathe."
        ]
    },
    "Full Black Coffee Rage ☕🔥": {
        "drinks": ["Triple-Shot Quad-Caffeine Espresso Bomb 💣", "Red Eye Cold Brew with Nitro Foam ⚡", "Dark Roast Pure Fury Espresso ☕"],
        "quotes": [
            "Channel the burn into productivity! Or at least intimidate the inbox.",
            "No sugar, no milk, no nonsense. Today we conquer through sheer caffeine.",
            "Pure power running through your veins. Handle with cute oven mitts!"
        ]
    }
}

CITIES = {
    "Nakuru, Kenya": (0.3031, 36.0800),
    "Nairobi, Kenya": (-1.286389, 36.817223),
    "London, UK": (51.5074, -0.1278),
    "New York, USA": (40.7128, -74.0060),
    "Tokyo, Japan": (35.6762, 139.6503),
    "Sydney, Australia": (-33.8688, 151.2093)
}

def hash_password(password: str) -> str:
    """Hash password securely using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def fetch_real_weather(city_name: str = "Nakuru, Kenya") -> Dict[str, Any]:
    """Fetch live temperature and conditions directly from Open-Meteo API."""
    lat, lon = CITIES.get(city_name, (0.3031, 36.0800))
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        current = data.get("current_weather", {})
        temp = current.get("temperature", 22.0)
        code = current.get("weathercode", 0)
        
        if code == 0:
            desc = "Clear Sky ☀️"
        elif code in [1, 2, 3]:
            desc = "Partly Cloudy ⛅"
        elif code in [45, 48]:
            desc = "Foggy 🌫️"
        elif code in [51, 61, 80]:
            desc = "Light Rain 🌧️"
        elif code in [63, 65, 81, 82]:
            desc = "Heavy Rain ⛈️"
        else:
            desc = "Overcast ☁️"
            
        return {"temp": temp, "desc": desc, "city": city_name}
    except Exception as e:
        logger.warning(f"Failed to fetch real weather data ({e}). Returning fallback weather.")
        return {"temp": 22.5, "desc": "Cozy Weather ⛅", "city": city_name}

def update_user_streak(db: Session, user: User) -> int:
    """Dynamic check-in streak update."""
    today = date.today()
    if user.last_checkin_date is None:
        user.current_streak = 1
    elif user.last_checkin_date == today:
        pass
    elif user.last_checkin_date == today - timedelta(days=1):
        user.current_streak += 1
    else:
        user.current_streak = 1
        
    user.last_checkin_date = today
    db.commit()
    db.refresh(user)
    return user.current_streak

INJECT_ANIMATED_CSS = """
<style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #FFFBEB, #FEF3C7, #FDE68A, #F59E0B);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated Pulsing Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #D97706, #B45309) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 15px rgba(217, 119, 6, 0.4);
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.03);
        box-shadow: 0px 6px 20px rgba(217, 119, 6, 0.6);
    }
    
    /* Glassmorphism Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: bold;
        color: #78350F;
    }
</style>
"""
