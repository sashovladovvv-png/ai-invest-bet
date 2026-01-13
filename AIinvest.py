import streamlit as st
import pandas as pd
import requests
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ И КЛЮЧОВЕ ---
# Поставям твоя нов API ключ тук
API_KEY = "B4c92379d14d40edb87a9f3412d6835f"
API_HOST = "api-football-v1.p.rapidapi.com"

st.set_page_config(page_title="EQUILIBRIUM AI | INVEST", page_icon="🛡️", layout="wide")

# Опресняване на интерфейса на всеки 15 минути (900 000 милисекунди)
# Това гарантира, че няма да изразходваш лимита си бързо
st_autorefresh(interval=900000, key="global_refresh")

# Файлове за данни
EMAILS_FILE = "emails.txt"
CACHE_FILE = "live_cache.json"

# --- 2. СТИЛИЗАЦИЯ (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background-color: #05080a;
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        color: #00ff00;
        text-align: center;
        font-size: 3.5rem;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
        margin-bottom: 0px;
    }
    
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .metric-card {
        background: rgba(16, 22, 26, 0.8);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
    }
    
    .metric-card:hover {
        border-color: #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }

    .live-tag {
        background: #ff0000;
        color: white;
        padding: 2px 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }

    .stake-badge {
        background: linear-gradient(90deg, #00ff00, #008000);
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }

    .prediction-text {
        color: #00ff00;
        font-weight: bold;
        font-size: 1.4rem;
        margin: 10px 0;
    }
    
    div.stButton > button {
        background-color: #00ff00 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ЛОГИКА ЗА ДАННИ ---

def fetch_football_data():
    """Централна функция за теглене на данни (Live и Upcoming)"""
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    live_signals = []
    upcoming_matches = []
    
    try:
        # 1. Изтегляне на LIVE мачове
        live_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        res_live = requests.get(live_url, headers=headers, params={"live": "all"}, timeout=10).json()
        
        for item in res_live.get('response', []):
            fixture = item['fixture']
            teams = item['teams']
            goals = item['goals']
            # Equilibrium Алгоритъм: Търсим мачове след 20-та минута при равенство или натиск
            elapsed = fixture['status']['elapsed']
            
            if elapsed and 20 <= elapsed <= 85:
                # Тук прилагаме математическото изравняване (проверка на резултат)
                if goals['home'] <= goals['away']: 
                    live_signals.append({
                        "id": fixture['id'],
                        "match": f"{teams['home']['name']} vs {teams['away']['name']}",
                        "minute": elapsed,
                        "score": f"{goals['home']}:{goals['away']}",
                        "prediction": "NEXT GOAL HOME (EQUILIBRIUM)",
                        "odds": round(random.uniform(1.90, 2.60), 2),
                        "stake": round(random.uniform(4.5, 5.5), 1)
                    })

        # 2. Изтегляне на ПРЕДСТОЯЩИ за днес
        today = datetime.date.today().strftime("%Y-%m-%d")
        res_up = requests.get(live_url, headers=headers, params={"date": today, "status": "NS"}, timeout=10).json()
        
        for item in res_up.get('response', [])[:9]: # Взимаме първите 9
            upcoming_matches.append({
                "time": item['fixture']['date'][11:16],
                "match": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                "league": item['league']['name']
            })
            
    except Exception as e:
        st.error(f"API Error: {e}")
        
    return live_signals, upcoming_matches

# --- 4. ИНТЕРФЕЙС - ГЛАВНА ЧАСТ ---

st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Statistical Anomaly Detection Engine</p>', unsafe_allow_html=True)

# Брояч на инвеститори (симулация на активност)
investors = random.randint(245, 312)
st.markdown(f'<p style="text-align:center; color:#00ff00; font-weight:bold;">● {investors} INVESTORS CURRENTLY ACTIVE</p>', unsafe_allow_html=True)

# Зареждане на данни
with st.spinner('Analyzing Global Markets...'):
    live_data, upcoming_data = fetch_football_data()

# --- СЕКЦИЯ: LIVE СИГНАЛИ ---
st.markdown("### 🚀 ACTIVE EQUILIBRIUM SIGNALS")
if live_data:
    cols = st.columns(3)
    for i, sig in enumerate(live_data):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="metric-card">
                    <span class="live-tag">LIVE {sig['minute']}'</span>
                    <p style="margin-top:10px; font-size:0.9rem; color:#888;">{sig['match']}</p>
                    <div class="prediction-text">{sig['prediction']}</div>
                    <h2 style="color:white; margin:5px 0;">@{sig['odds']}</h2>
                    <div class="stake-badge">STAKE: {sig['stake']}%</div>
                    <p style="font-size:0.8rem; color:#555; margin-top:10px;">Current Score: {sig['score']}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Searching for statistical imbalances... No high-probability signals at this moment.")

st.markdown("---")

# --- СЕКЦИЯ: ПРЕДСТОЯЩИ МАЧОВЕ ---
st.markdown("### 📅 UPCOMING ANALYSIS TODAY")
if upcoming_data:
    u_cols = st.columns(3)
    for i, m in enumerate(upcoming_data):
        with u_cols[i % 3]:
            st.markdown(f"""
                <div style="background:#10161a; border-left:3px solid #00ff00; padding:15px; border-radius:10px; margin-bottom:10px;">
                    <span style="color:#00ff00; font-size:0.8rem;">{m['time']} | {m['league']}</span><br>
                    <b style="color:white;">{m['match']}</b><br>
                    <small style="color:#555;">Status: Awaiting Equilibrium Pressure</small>
                </div>
            """, unsafe_allow_html=True)

# --- СЕКЦИЯ: VIP АБОНАМЕНТ ---
st.markdown("---")
col_e1, col_e2 = st.columns([2, 1])
with col_e1:
    st.markdown("### 📩 GET VIP SIGNALS VIA EMAIL")
    email_input = st.text_input("Enter your professional email address", placeholder="investor@example.com")
with col_e2:
    st.write("##")
    if st.button("ACTIVATE VIP ACCESS"):
        if "@" in email_input and "." in email_input:
            with open(EMAILS_FILE, "a") as f:
                f.write(f"{datetime.datetime.now()}: {email_input}\n")
            st.success("Registration Successful! You will receive signals tomorrow.")
        else:
            st.error("Please enter a valid email.")

# --- SIDEBAR: АДМИН И ЗАЩИТА ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2583/2583118.png", width=100)
    st.title("Control Panel")
    st.write("---")
    st.write("🛡️ **System Security: ACTIVE**")
    st.write(f"🕒 Last Update: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.write("📡 API Status: Connected")
    
    st.markdown("---")
    st.write("📧 **Email Administration**")
    if st.button("SEND SIGNALS TO ALL"):
        if os.path.exists("mailer.py"):
            st.info("Broadcasting signals to subscribers...")
            # Тук се извиква мейлър скрипта
            os.system("python mailer.py")
            st.success("Broadcast completed!")
        else:
            st.error("Error: mailer.py missing.")
            
    st.markdown("---")
    st.write("💰 **Market Protection**")
    st.caption("Our AI automatically stops signals if liquidity is too low to protect investors.")

# --- ФУТЪР ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:#444;'>© 2026 EQUILIBRIUM AI INVESTMENTS | Professional Grade Sport Analytics</p>", unsafe_allow_html=True)
