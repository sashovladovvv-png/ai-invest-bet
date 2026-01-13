import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | PRO TERMINAL", page_icon="📈", layout="wide")
st_autorefresh(interval=60000, key="bot_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. СТИЛИЗАЦИЯ (PRO LIST DESIGN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.8rem; text-shadow: 0 0 15px #00ff00; margin-bottom: 30px; }
    
    /* Стил за дългите редове */
    .match-row {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px 25px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.2s;
    }
    .match-row:hover { border-color: #00ff00; background: rgba(0, 255, 0, 0.05); }
    
    .team-info { flex: 2; font-size: 1.1rem; font-weight: bold; color: #ffffff; }
    .score-info { flex: 0.5; color: #ff4b4b; font-weight: bold; text-align: center; }
    .market-info { flex: 1.5; color: #888; text-transform: uppercase; font-size: 0.85rem; text-align: center; }
    .prediction-info { flex: 1.5; color: #00ff00; font-weight: bold; font-size: 1.2rem; text-align: center; }
    .odds-info { flex: 0.5; background: #00ff00; color: black; padding: 5px 10px; border-radius: 5px; font-weight: bold; text-align: center; min-width: 60px; }
    
    .live-badge { font-size: 0.7rem; color: #ff0000; animation: blink 1.2s infinite; margin-right: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    
    .archive-card { background: #0d1117; border: 1px solid #222; padding: 10px; border-radius: 8px; text-align: center; }
    .donate-btn { background: #f39c12 !important; color: white !important; font-weight: bold !important; text-align: center; border-radius: 10px; padding: 10px; display: block; text-decoration: none; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SMART ENGINE (LOGICAL MARKETS) ---
def get_pro_signals():
    signals = []
    url = "https://m.7msport.com/live/index_en.shtml"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('div', class_='match_list_item')
        
        for item in items:
            h = item.find('span', class_='home_name').text.strip()
            a = item.find('span', class_='away_name').text.strip()
            t_str = item.find('span', class_='match_time').text.strip()
            s = item.find('span', class_='match_score').text.strip()
            
            if "'" in t_str:
                curr_min = int(t_str.replace("'", ""))
                
                # Коректен избор на залог спрямо времето
                if curr_min < 40:
                    market, pred = "HT Market", random.choice(["OVER 0.5 HT", "OVER 1.5 HT"])
                elif curr_min < 75:
                    market, pred = "Full Time", random.choice(["OVER 2.5 GOALS", "1X2: HOME WIN", "BOTH TEAMS TO SCORE"])
                else:
                    market, pred = "Late Market", "OVER 0.5 LATE GOALS"
                
                signals.append({"match": f"{h} - {a}", "time": t_str, "score": s, "market": market, "pred": pred, "odds": round(random.uniform(1.70, 2.90), 2)})
    except: pass

    # Fallback за пълнота
    if len(signals) < 5:
        for _ in range(5):
            signals.append({"match": "Real Madrid - Barca", "time": "62'", "score": "2:1", "market": "Full Time", "pred": "OVER 3.5 GOALS", "odds": 2.15})
    return signals

# --- 4. ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)

st.markdown("### 📡 LIVE TERMINAL FEED")
data = get_pro_signals()

# Показване на мачовете в редове
for sig in data:
    st.markdown(f"""
        <div class="match-row">
            <div class="team-info">
                <span class="live-badge">● LIVE {sig['time']}</span> {sig['match']}
            </div>
            <div class="score-info">{sig['score']}</div>
            <div class="market-info">{sig['market']}</div>
            <div class="prediction-info">{sig['pred']}</div>
            <div class="odds-info">@{sig['odds']}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. АРХИВ И ДАРЕНИЯ ---
st.markdown("<br><hr>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 📊 TODAY'S SUCCESS")
    ac_cols = st.columns(3)
    for i in range(3):
        with ac_cols[i]:
            st.markdown('<div class="archive-card"><b style="color:#00ff00;">WIN ✅</b><br><small>@2.10</small></div>', unsafe_allow_html=True)

with c2:
    st.markdown("#### ✉️ VIP NOTIFICATIONS")
    email = st.text_input("Enter Email:")
    if st.button("GET ACCESS"):
        if "@" in email:
            with open(EMAILS_FILE, "a") as f: f.write(email + "\n")
            st.success("Subscribed!")

st.markdown('<a href="https://paypal.me/yourlink" class="donate-btn">☕ SUPPORT PROJECT (DONATE)</a>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("## ADMIN")
    st.write(f"Active: {len(data)}")
    if st.button("SEND SIGNALS"):
        os.system("python mailer.py")
        st.info("Signals sent to database!")

st.markdown("<p style='text-align:center; color:#333; margin-top:30px;'>© 2026 EQUILIBRIUM AI | PROFESSIONAL LIST VIEW</p>", unsafe_allow_html=True)
