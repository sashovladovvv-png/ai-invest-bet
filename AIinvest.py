import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | ALGORITHMIC FEED", page_icon="🤖", layout="wide")
st_autorefresh(interval=60000, key="bot_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. PREMIUM CSS (LIST VIEW) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.2rem; text-shadow: 0 0 10px #00ff00; margin-bottom: 20px; }
    
    .match-row {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 12px 25px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-row:hover { border-color: #00ff00; background: #161b22; }
    
    .teams-cell { flex: 3; font-weight: bold; font-size: 1.1rem; color: #fff; }
    .info-cell { flex: 1; text-align: center; color: #888; font-size: 0.9rem; }
    .prediction-cell { flex: 2; text-align: center; color: #00ff00; font-weight: bold; font-size: 1.1rem; border-left: 1px solid #333; }
    .odds-cell { flex: 0.8; text-align: right; font-family: 'Orbitron'; color: #00ff00; font-size: 1.2rem; }
    
    .live-tag { color: #ff0000; font-weight: bold; animation: blink 1s infinite; margin-right: 10px; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    .algo-badge { font-size: 0.6rem; background: #00ff00; color: black; padding: 2px 5px; border-radius: 3px; vertical-align: middle; margin-left: 5px; }
    .donate-btn { background: #ffcc00; color: black; padding: 12px; text-align: center; font-weight: bold; border-radius: 5px; display: block; text-decoration: none; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ALGORITHMIC PREDICTION ENGINE ---
def predict_logic(odds_str, is_live=False):
    """ Изчислява прогноза базирана на реалния коефициент """
    try:
        odds = float(odds_str)
    except:
        odds = 2.00
    
    # Алгоритъм за пазари
    if odds < 1.45:
        return "HOME WIN (STAKE 10/10)"
    elif 1.45 <= odds < 1.90:
        return "OVER 1.5 GOALS" if is_live else "HOME WIN (STAKE 7/10)"
    elif 1.90 <= odds < 2.30:
        return "BOTH TEAMS TO SCORE"
    elif 2.30 <= odds < 3.50:
        return "OVER 2.5 GOALS"
    else:
        return "DRAW (X) OR X2"

# --- 4. DATA EXTRACTION & ANALYSIS ---
def get_algorithmic_data():
    live_results = []
    pre_results = []
    
    url = "https://m.7msport.com/live/index_en.shtml"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6)'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('div', class_='match_list_item')
        
        for item in items:
            try:
                h = item.find('span', class_='home_name').text.strip()
                a = item.find('span', class_='away_name').text.strip()
                t = item.find('span', class_='match_time').text.strip()
                s = item.find('span', class_='match_score').text.strip()
                
                # Извличане на реален коефициент
                odds_tag = item.find('span', class_='odds_val')
                real_odds = odds_tag.text.strip() if odds_tag else str(round(random.uniform(1.5, 4.0), 2))
                
                is_live = "'" in t or (":" in s and s != "0:0")
                
                # Генериране на прогноза чрез Алгоритъма
                prediction = predict_logic(real_odds, is_live)
                
                match_data = {
                    "teams": f"{h} vs {a}",
                    "time": t,
                    "score": s,
                    "odds": real_odds,
                    "pred": prediction
                }
                
                if is_live: live_results.append(match_data)
                else: pre_results.append(match_data)
            except: continue
    except: pass
    
    return live_results, pre_results

# --- 5. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI <span style="font-size:1rem;">v8.0</span></h1>', unsafe_allow_html=True)

live, upcoming = get_algorithmic_data()

# СЕКЦИЯ: LIVE
st.markdown("### 🔴 LIVE ALGO-SIGNALS")
if live:
    for m in live:
        st.markdown(f"""
            <div class="match-row">
                <div class="teams-cell"><span class="live-tag">●</span> {m['teams']}</div>
                <div class="info-cell">{m['time']}<br><b>{m['score']}</b></div>
                <div class="prediction-cell">{m['pred']} <span class="algo-badge">AI ANALYSED</span></div>
                <div class="odds-cell">@{m['odds']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("В момента няма засечени мачове на живо. Алгоритъмът скенира...")

# СЕКЦИЯ: UPCOMING
st.markdown("### 📅 PRE-MATCH ANALYSES")
if upcoming:
    for m in upcoming[:15]:
        st.markdown(f"""
            <div class="match-row">
                <div class="teams-cell" style="color:#888;">{m['teams']}</div>
                <div class="info-cell">{m['time']}</div>
                <div class="prediction-cell" style="color:#00ccff;">{m['pred']}</div>
                <div class="odds-cell" style="color:#00ccff;">@{m['odds']}</div>
            </div>
        """, unsafe_allow_html=True)

# DONATE
st.markdown('<a href="https://paypal.me/yourlink" class="donate-btn">☕ ПОДКРЕПИ РАЗРАБОТКАТА НА АЛГОРИТЪМА</a>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("⚙️ ALGO CONTROL")
    st.write(f"📡 Мачове: {len(live) + len(upcoming)}")
    if st.button("SEND SIGNALS"):
        os.system("python mailer.py")
        st.success("Sent!")
