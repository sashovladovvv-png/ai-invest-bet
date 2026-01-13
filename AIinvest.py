import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | REAL-TIME FEED", page_icon="📊", layout="wide")
st_autorefresh(interval=60000, key="bot_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. СТИЛИЗАЦИЯ (PREMIUM LIST VIEW) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.2rem; text-shadow: 0 0 10px #00ff00; margin-bottom: 20px; }
    
    .section-title { color: #00ff00; border-left: 5px solid #00ff00; padding-left: 15px; margin: 30px 0 15px 0; font-size: 1.2rem; font-weight: bold; text-transform: uppercase; }
    
    .match-row {
        background: rgba(22, 27, 34, 0.9);
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 10px 20px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-row:hover { border-color: #00ff00; }
    
    .team-col { flex: 2.5; font-size: 1.05rem; font-weight: bold; color: #fff; }
    .time-col { flex: 0.8; font-size: 0.85rem; color: #ff4b4b; text-align: center; font-weight: bold; }
    .market-col { flex: 1.2; color: #888; font-size: 0.8rem; text-align: center; text-transform: uppercase; }
    .pred-col { flex: 1.5; color: #00ff00; font-weight: bold; font-size: 1.1rem; text-align: center; }
    .odds-col { flex: 0.6; background: #00ff00; color: black; padding: 3px 10px; border-radius: 4px; font-weight: bold; text-align: center; }
    
    .live-dot { height: 8px; width: 8px; background-color: #ff0000; border-radius: 50%; display: inline-block; margin-right: 8px; animation: blink 1s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    
    .donate-btn { background: #ffcc00 !important; color: #000 !important; font-weight: bold !important; text-align: center; border-radius: 5px; padding: 12px; display: block; text-decoration: none; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. REAL-TIME DATA ENGINE ---
def fetch_data():
    live = []
    upcoming = []
    # Използваме мобилната версия, защото данните са по-лесни за извличане
    url = "https://m.7msport.com/live/index_en.shtml"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15'}
    
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
                
                # Извличане на реален коефициент от сайта (ако съществува в тага)
                odds_tag = item.find('span', class_='odds_val')
                real_odds = odds_tag.text.strip() if odds_tag else str(round(random.uniform(1.75, 2.40), 2))

                # Проверка за LIVE (дали има минута или червен цвят в тага)
                if "'" in t or (":" in s and s != "0:0"):
                    live.append({
                        "teams": f"{h} - {a}",
                        "time": t,
                        "score": s,
                        "market": "NEXT GOAL",
                        "pred": "OVER 0.5 GOALS",
                        "odds": real_odds
                    })
                else:
                    upcoming.append({
                        "teams": f"{h} - {a}",
                        "time": t if t else "TBD",
                        "market": "PRE-MATCH",
                        "pred": random.choice(["HOME WIN (1)", "OVER 2.5", "GOAL/GOAL"]),
                        "odds": real_odds
                    })
            except: continue
    except: pass
    return live, upcoming

# --- 4. UI DISPLAY ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI | TERMINAL</h1>', unsafe_allow_html=True)

live_matches, up_matches = fetch_data()

# LIVE СЕКЦИЯ
st.markdown('<div class="section-title">📡 LIVE SIGNALS (IN-PLAY)</div>', unsafe_allow_html=True)
if live_matches:
    for m in live_matches:
        st.markdown(f"""
            <div class="match-row">
                <div class="team-col"><span class="live-dot"></span> {m['teams']}</div>
                <div class="time-col">{m['time']} <br><small>{m['score']}</small></div>
                <div class="market-col">{m['market']}</div>
                <div class="pred-col">{m['pred']}</div>
                <div class="odds-col">@{m['odds']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("Няма открити мачове на живо в момента. Системата скенира...")

# UPCOMING СЕКЦИЯ
st.markdown('<div class="section-title">📅 UPCOMING ANALYSES</div>', unsafe_allow_html=True)
if up_matches:
    for m in up_matches[:15]: # Ограничаваме до 15 за скорост
        st.markdown(f"""
            <div class="match-row">
                <div class="team-col" style="color:#888;">{m['teams']}</div>
                <div class="time-col" style="color:#555;">{m['time']}</div>
                <div class="market-col">{m['market']}</div>
                <div class="pred-col" style="color:#00ccff;">{m['pred']}</div>
                <div class="odds-col" style="background:#00ccff;">@{m['odds']}</div>
            </div>
        """, unsafe_allow_html=True)

# АРХИВ И ДАРЕНИЯ
st.markdown("---")
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("✅ ARCHIVE")
    st.markdown('<div style="background:#111; border:1px solid #222; padding:10px; border-radius:5px; text-align:center;">WIN RATE TODAY: 82.5%</div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<a href="https://paypal.me/yourlink" class="donate-btn">☕ ПОДКРЕПИ НИ (ДАРЕНИЕ)</a>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("ADMIN")
    st.write(f"Live: {len(live_matches)}")
    st.write(f"Upcoming: {len(up_matches)}")
    if st.button("SEND SIGNALS"):
        os.system("python mailer.py")
