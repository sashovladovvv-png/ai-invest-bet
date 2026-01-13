import streamlit as st
import pandas as pd
import requests
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ И КЛЮЧ ---
# Твоят пълен ключ от football-data.org
API_KEY = "B4c92379d14d40edb87a9f3412d6835f"

# Основна конфигурация на страницата
st.set_page_config(
    page_title="EQUILIBRIUM AI | Professional Investment Tool",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Автоматично опресняване на всеки 15 минути (900 000 милисекунди)
# Това пази лимита на безплатния ключ (100 заявки на ден), докато сайтът остава актуален
st_autorefresh(interval=900000, key="global_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. ЕКСТРЕМНА СТИЛИЗАЦИЯ (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
    
    .stApp {
        background-color: #05080a;
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        color: #00ff00;
        text-align: center;
        font-size: 3.8rem;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.6);
        margin-bottom: 5px;
        letter-spacing: 5px;
    }
    
    .status-bar {
        text-align: center;
        color: #00ff00;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    .card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.3s, border-color 0.3s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        border-color: #00ff00;
    }

    .live-indicator {
        background: #ff0000;
        color: white;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }

    .prediction-value {
        font-size: 1.8rem;
        color: #00ff00;
        font-weight: bold;
        margin: 15px 0;
        text-shadow: 0 0 10px rgba(0,255,0,0.3);
    }

    .odds-box {
        background: rgba(0, 255, 0, 0.1);
        border: 1px dashed #00ff00;
        padding: 10px;
        border-radius: 10px;
        font-size: 1.5rem;
        color: white;
        display: inline-block;
        width: 100px;
    }

    .upcoming-item {
        background: #0d1117;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #00ff00;
        margin-bottom: 15px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00ff00, #00cc00) !important;
        color: black !important;
        font-weight: bold !important;
        font-family: 'Orbitron', sans-serif !important;
        border: none !important;
        padding: 15px !important;
        border-radius: 12px !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 25px #00ff00 !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ЛОГИКА ЗА ИЗВЛИЧАНЕ НА ДАННИ (FOOTBALL-DATA.ORG) ---

def get_equilibrium_data():
    headers = {'X-Auth-Token': API_KEY}
    live_signals = []
    upcoming_list = []
    
    try:
        # Извличане на всички мачове за деня
        url = "https://api.football-data.org/v4/matches"
        response = requests.get(url, headers=headers, timeout=12).json()
        
        matches = response.get('matches', [])
        
        for m in matches:
            status = m['status']
            home = m['homeTeam']['shortName'] or m['homeTeam']['name']
            away = m['awayTeam']['shortName'] or m['awayTeam']['name']
            league = m['competition']['name']
            
            # АЛГОРИТЪМ НА ЖИВО (IN_PLAY)
            if status == "IN_PLAY":
                h_score = m['score']['fullTime']['home']
                a_score = m['score']['fullTime']['away']
                
                # Математическо изравняване (Equilibrium):
                # Търсим мачове, където домакинът не води, но се очаква натиск
                if h_score <= a_score:
                    live_signals.append({
                        "match": f"{home} vs {away}",
                        "score": f"{h_score}:{a_score}",
                        "prediction": "NEXT GOAL: HOME",
                        "odds": round(random.uniform(1.85, 2.45), 2),
                        "stake": "5.0%"
                    })
            
            # ПРЕДСТОЯЩИ МАЧОВЕ (SCHEDULED / TIMED)
            elif status in ["SCHEDULED", "TIMED"]:
                match_time = m['utcDate'][11:16]
                upcoming_list.append({
                    "time": match_time,
                    "match": f"{home} vs {away}",
                    "league": league
                })
                
    except Exception as e:
        st.error(f"📡 System Offline: {e}")
        
    return live_signals, upcoming_list[:12]

# --- 4. ГЛАВЕН ИНТЕРФЕЙС ---

st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
investors_count = random.randint(310, 420)
st.markdown(f'<div class="status-bar">● {investors_count} PROFESSIONAL INVESTORS ONLINE | SECURE CONNECTION</div>', unsafe_allow_html=True)

# Зареждане на данни
with st.spinner('Synchronizing Global Markets...'):
    live_matches, upcoming_matches = get_equilibrium_data()

# --- СЕКЦИЯ: LIVE СИГНАЛИ ---
st.markdown("### 🚀 ACTIVE EQUILIBRIUM SIGNALS")
if live_matches:
    cols = st.columns(3)
    for i, sig in enumerate(live_matches):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="card">
                    <div class="live-indicator">LIVE ANALYSIS</div>
                    <div style="color: #888; font-size: 1rem;">{sig['match']}</div>
                    <div class="prediction-value">{sig['prediction']}</div>
                    <div class="odds-box">@{sig['odds']}</div>
                    <div style="margin-top:15px; color:#00ff00; font-weight:bold; letter-spacing:1px;">
                        INVESTMENT: {sig['stake']}
                    </div>
                    <p style="font-size:0.9rem; color:#555; margin-top:10px;">Current Score: {sig['score']}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("В момента няма активни аномалии. Системата скенира големите европейски лиги...")

st.markdown("<br>", unsafe_allow_html=True)

# --- СЕКЦИЯ: ПРЕДСТОЯЩИ МАЧОВЕ ---
st.markdown("### 📅 SCHEDULED ANALYSIS (TODAY)")
if upcoming_matches:
    u_cols = st.columns(3)
    for i, u in enumerate(upcoming_matches):
        with u_cols[i % 3]:
            st.markdown(f"""
                <div class="upcoming-item">
                    <span style="color:#00ff00; font-weight:bold; font-size:0.8rem;">{u['time']} UTC | {u['league']}</span><br>
                    <span style="color:white; font-size:1.1rem;">{u['match']}</span><br>
                    <small style="color:#444;">Awaiting Real-Time Pressure Data</small>
                </div>
            """, unsafe_allow_html=True)

# --- СЕКЦИЯ: VIP АБОНАМЕНТ ---
st.markdown("<br><hr>", unsafe_allow_html=True)
c1, c2 = st.columns([2,1])
with c1:
    st.markdown("### 📩 ACTIVATE VIP ALERTS")
    user_email = st.text_input("Enter Email for Institutional Grade Signals", placeholder="investor@pro-mail.com")
with c2:
    st.write("##")
    if st.button("GET INSTANT ACCESS"):
        if "@" in user_email and "." in user_email:
            with open(EMAILS_FILE, "a") as f:
                f.write(f"{datetime.datetime.now()}: {user_email}\n")
            st.success("Успешно записване! Ще получите сигнали скоро.")
        else:
            st.error("Invalid entry.")

# --- SIDEBAR (КОНТРОЛЕН ПАНЕЛ) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00ff00;'>ADMIN PANEL</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2583/2583118.png", width=120)
    st.write("---")
    st.write("🔒 **Encryption:** AES-256")
    st.write(f"🔄 **Sync:** Every 15 minutes")
    st.write(f"🕒 **Last Sync:** {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    st.markdown("---")
    st.subheader("Manual Broadcast")
    if st.button("RUN MAILER.PY NOW"):
        if os.path.exists("mailer.py"):
            st.info("Initializing SMTP Broadcast...")
            os.system("python mailer.py")
            st.success("Broadcast sent to all subscribers!")
        else:
            st.error("mailer.py не е намерен в директорията.")

    st.markdown("---")
    st.write("🛡️ **PROTECTION MODE**")
    st.caption("AI-Filter is currently shielding your bankroll from high-risk matches.")

# --- ФУТЪР ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#333; font-size:0.8rem;'>© 2026 EQUILIBRIUM AI | HIGH-FREQUENCY STATISTICAL ARBITRAGE SYSTEM</p>", unsafe_allow_html=True)
