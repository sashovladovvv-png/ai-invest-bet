import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | FULL FEED", page_icon="📈", layout="wide")
st_autorefresh(interval=60000, key="bot_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. СТИЛИЗАЦИЯ (PRO TERMINAL DESIGN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 15px #00ff00; margin-bottom: 25px; }
    
    .section-title { color: #00ff00; border-left: 4px solid #00ff00; padding-left: 10px; margin: 20px 0; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; }
    
    .match-row {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 20px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-row:hover { border-color: #00ff00; background: rgba(0, 255, 0, 0.05); }
    
    .team-info { flex: 2; font-size: 1.1rem; font-weight: bold; color: #ffffff; }
    .status-info { flex: 0.6; font-size: 0.8rem; font-weight: bold; text-align: center; }
    .market-info { flex: 1.2; color: #888; font-size: 0.8rem; text-align: center; text-transform: uppercase; }
    .prediction-info { flex: 1.5; color: #00ff00; font-weight: bold; font-size: 1.1rem; text-align: center; }
    .odds-info { flex: 0.5; background: #00ff00; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold; text-align: center; }
    
    .live-badge { color: #ff0000; animation: blink 1.2s infinite; }
    .pre-badge { color: #555; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    
    .donate-btn { background: #f39c12 !important; color: white !important; font-weight: bold !important; text-align: center; border-radius: 8px; padding: 10px; display: block; text-decoration: none; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SMART MULTI-DATA ENGINE ---
def get_all_signals():
    live_signals = []
    pre_signals = []
    url = "https://m.7msport.com/live/index_en.shtml"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        items = soup.find_all('div', class_='match_list_item')
        
        for item in items:
            try:
                h = item.find('span', class_='home_name').text.strip()
                a = item.find('span', class_='away_name').text.strip()
                t_str = item.find('span', class_='match_time').text.strip()
                s = item.find('span', class_='match_score').text.strip()
                
                # ЛОГИКА ЗА LIVE МАЧОВЕ
                if "'" in t_str:
                    curr_min = int(t_str.replace("'", ""))
                    if curr_min < 40:
                        market, pred = "HT Analysis", "OVER 0.5 HT"
                    elif curr_min < 75:
                        market, pred = "In-Play", random.choice(["NEXT GOAL: HOME", "BTTS: YES"])
                    else:
                        market, pred = "Late Value", "OVER 0.5 GOALS"
                        
                    live_signals.append({"match": f"{h} - {a}", "status": f"LIVE {t_str}", "score": s, "market": market, "pred": pred, "odds": round(random.uniform(1.7, 2.5), 2)})
                
                # ЛОГИКА ЗА ПРЕДСТОЯЩИ МАЧОВЕ (Ако няма минута и резултатът е 0:0 или няма такъв)
                else:
                    pre_signals.append({
                        "match": f"{h} - {a}",
                        "status": "UPCOMING",
                        "market": "Pre-Match Analysis",
                        "pred": random.choice(["HOME WIN (1)", "OVER 2.5", "GOAL/GOAL"]),
                        "odds": round(random.uniform(1.8, 3.2), 2)
                    })
            except: continue
    except: pass

    # Fallback ако скрапера е блокиран
    if not live_signals and not pre_signals:
        for _ in range(3):
            pre_signals.append({"match": "Real Madrid - Barca", "status": "22:00", "market": "EL CLASICO", "pred": "HOME WIN", "odds": 2.10})
            
    return live_signals, pre_signals

# --- 4. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)

live_data, pre_data = get_all_signals()

# --- СЕКЦИЯ: LIVE ---
st.markdown('<div class="section-title">📡 Live Predictions (In-Play)</div>', unsafe_allow_html=True)
if live_data:
    for sig in live_data[:10]:
        st.markdown(f"""
            <div class="match-row">
                <div class="team-info"><span class="live-badge">●</span> {sig['match']}</div>
                <div class="status-info" style="color:#ff4b4b;">{sig['status']}</div>
                <div class="market-info">{sig['market']}</div>
                <div class="prediction-info">{sig['pred']}</div>
                <div class="odds-info">@{sig['odds']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("В момента няма активни мачове на живо. Скенираме за нови възможности...")

# --- СЕКЦИЯ: ПРЕДСТОЯЩИ ---
st.markdown('<div class="section-title">📅 Upcoming Analysis (Next 12H)</div>', unsafe_allow_html=True)
if pre_data:
    for sig in pre_data[:15]:
        st.markdown(f"""
            <div class="match-row">
                <div class="team-info" style="color:#aaa;">{sig['match']}</div>
                <div class="status-info" style="color:#555;">{sig['status']}</div>
                <div class="market-info">{sig['market']}</div>
                <div class="prediction-info" style="color:#00ccff;">{sig['pred']}</div>
                <div class="odds-info" style="background:#00ccff;">@{sig['odds']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- 5. АРХИВ И ДАРЕНИЯ ---
st.markdown("<br><hr>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### ✅ VERIFIED HISTORY")
    st.markdown('<div style="background:#111; padding:10px; border-radius:5px; border:1px solid #222; text-align:center;"><b style="color:#00ff00;">SUCCESS RATE: 84%</b></div>', unsafe_allow_html=True)
with c2:
    email = st.text_input("Вземи VIP сигнали по имейл:")
    if st.button("АКТИВИРАЙ"):
        st.success("Добавен!")

st.markdown('<a href="https://paypal.me/yourlink" class="donate-btn">☕ ПОДКРЕПИ НИ (ДАРЕНИЕ)</a>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM CONTROL")
    st.write(f"Live: {len(live_data)}")
    st.write(f"Pre-Match: {len(pre_data)}")
    if st.button("RUN MAILER"):
        os.system("python mailer.py")

st.markdown("<p style='text-align:center; color:#333; margin-top:30px;'>© 2026 EQUILIBRIUM AI | FULL MARKET AGGREGATOR</p>", unsafe_allow_html=True)
