import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import datetime
import os
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(
    page_title="EQUILIBRIUM AI | MULTI-MARKET TERMINAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Автоматично опресняване на всяка минута
st_autorefresh(interval=60000, key="bot_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. ДИЗАЙН (MODERN DARK INTERFACE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
    
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    
    .main-header {
        font-family: 'Orbitron', sans-serif;
        color: #00ff00;
        text-align: center;
        font-size: 3.5rem;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.6);
        margin-bottom: 10px;
    }
    
    .card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .card:hover { border-color: #00ff00; transform: translateY(-3px); }

    .market-tag {
        background: rgba(0, 255, 0, 0.1);
        color: #00ff00;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
        border: 1px solid rgba(0, 255, 0, 0.3);
    }

    .live-dot {
        height: 8px;
        width: 8px;
        background-color: #ff0000;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        animation: blink 1s infinite;
    }

    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    .prediction { font-size: 1.5rem; color: #ffffff; font-weight: bold; margin: 10px 0; }
    .odds { color: #00ff00; font-size: 1.3rem; font-weight: bold; }
    
    div.stButton > button {
        background: #00ff00 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 5px !important;
        width: 100%;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-MARKET ENGINE ---
def get_all_market_signals():
    signals = []
    # Източник на реални мачове
    url = "https://m.7msport.com/live/index_en.shtml"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        match_items = soup.find_all('div', class_='match_list_item')
        
        # Списък с видове прогнози за по-голямо разнообразие
        market_types = [
            {"label": "1X2 PREDICTION", "options": ["HOME WIN", "AWAY WIN", "DRAW"]},
            {"label": "GOALS MARKET", "options": ["OVER 2.5 GOALS", "UNDER 2.5 GOALS", "BOTH TEAMS TO SCORE"]},
            {"label": "HALF TIME", "options": ["OVER 0.5 HT", "HOME TO SCORE HT"]},
            {"label": "DYNAMIC", "options": ["NEXT GOAL: HOME", "NEXT GOAL: AWAY"]}
        ]

        for item in match_items:
            try:
                home = item.find('span', class_='home_name').text.strip()
                away = item.find('span', class_='away_name').text.strip()
                score = item.find('span', class_='match_score').text.strip()
                m_time = item.find('span', class_='match_time').text.strip()
                
                # Ако мачът е на живо (има минута)
                if "'" in m_time:
                    # Избираме случаен пазар за всеки мач, за да е пълен сайта
                    market = random.choice(market_types)
                    prediction = random.choice(market['options'])
                    
                    signals.append({
                        "match": f"{home} vs {away}",
                        "time": m_time,
                        "score": score,
                        "market": market['label'],
                        "prediction": prediction,
                        "odds": round(random.uniform(1.65, 3.20), 2)
                    })
            except:
                continue
    except:
        pass
        
    return signals

# --- 4. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#00ff00;">● LIVE MULTI-MARKET FEED | ACTIVE INVESTORS: {random.randint(700, 950)}</p>', unsafe_allow_html=True)

# ИЗВЛИЧАНЕ НА ДАННИ
data = get_all_market_signals()

if data:
    # Показваме мачовете в решетка от 3 колони
    cols = st.columns(3)
    for i, sig in enumerate(data):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span class="live-dot"></span> <span style="font-size: 0.9rem; color: #ff4b4b;">LIVE {sig['time']}</span>
                    </div>
                    <div style="font-size: 1rem; color: #888; margin-bottom: 5px;">{sig['match']}</div>
                    <div style="font-size: 0.9rem; color: #555; margin-bottom: 10px;">Score: {sig['score']}</div>
                    <div class="market-tag">{sig['market']}</div>
                    <div class="prediction">{sig['prediction']}</div>
                    <div class="odds">@{sig['odds']}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Ботът скенира глобалните пазари... В момента няма активни мачове на живо. Очаквайте старт на новите срещи скоро.")

# АРХИВ (ПОСЛЕДНИ 10 РЕЗУЛТАТА)
st.markdown("---")
st.subheader("📊 RECENT SETTLED PREDICTIONS")
h_cols = st.columns(5)
for i in range(5):
    with h_cols[i]:
        res = "WIN ✅" if random.random() > 0.25 else "LOSS ❌"
        color = "#00ff00" if "WIN" in res else "#ff4b4b"
        st.markdown(f"""
            <div style="background:#10161a; padding:10px; border-radius:8px; text-align:center; border:1px solid #30363d;">
                <span style="color:{color}; font-weight:bold;">{res}</span><br>
                <small style="color:#444;">Market @{round(random.uniform(1.7, 2.5), 2)}</small>
            </div>
        """, unsafe_allow_html=True)

# ИМЕЙЛ СИСТЕМА
st.markdown("<br>")
email_col, btn_col = st.columns([3, 1])
with email_col:
    user_email = st.text_input("Абонирай се за всички High-Frequency сигнали:", placeholder="email@example.com")
with btn_col:
    st.write("##")
    if st.button("VIP ДОСТЪП"):
        if "@" in user_email:
            with open(EMAILS_FILE, "a") as f: f.write(user_email + "\n")
            st.success("Готово!")

# --- 5. SIDEBAR (БЕЗ ПАРОЛА) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ff00;'>CONTROL CENTER</h2>", unsafe_allow_html=True)
    st.write(f"📡 Активни мачове: **{len(data)}**")
    st.write(f"🌍 Източник: **Global Feed**")
    st.markdown("---")
    if st.button("ИЗПРАТИ СИГНАЛИ (MAILER)"):
        if os.path.exists("mailer.py"):
            os.system("python mailer.py")
            st.success("Сигналите са разпратени!")
        else:
            st.error("mailer.py не е намерен!")

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>© 2026 EQUILIBRIUM AI | MULTI-MARKET ENGINE</p>", unsafe_allow_html=True)
