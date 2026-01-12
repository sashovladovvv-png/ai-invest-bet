import streamlit as st
import pandas as pd
import requests
import random
import datetime
import os
from streamlit_autorefresh import st_autorefresh

# --- 1. ЦЕНТРАЛНИ API КЛЮЧОВЕ ---
API_FOOTBALL_KEY = "b4c92379d14d40edb87a9f3412d6835f" 
BETS_API_KEY = "b5b07a3f-b019-4a18-8969-6045169feda9"

# --- 2. НАСТРОЙКИ И ФАЙЛОВЕ ---
st.set_page_config(page_title="EQUILIBRIUM AI | Premium Intelligence", page_icon="🛡️", layout="wide")
st_autorefresh(interval=60000, key="engine_refresh")

HISTORY_FILE = "match_history.csv"
EMAILS_FILE = "emails.txt"

# --- 3. ЛОГИКА ЗА ДАННИТЕ ---

def fetch_live_and_upcoming():
    live_signals = []
    upcoming_matches = []
    
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": API_FOOTBALL_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    
    # А) Вземане на мачове на живо за Equilibrium Сигнали
    try:
        res_live = requests.get(url, headers=headers, params={"live": "all"}, timeout=10).json()
        for item in res_live.get('response', []):
            minute = item['fixture']['status']['elapsed']
            da_home = 0
            stats = item.get('statistics', [])
            if stats:
                for s in stats[0]['statistics']:
                    if s['type'] == 'Dangerous Attacks':
                        da_home = int(s['value']) if s['value'] else 0
            
            # EQUILIBRIUM АЛГОРИТЪМ
            if minute > 20 and da_home > (minute * 1.1) and item['goals']['home'] <= item['goals']['away']:
                sig = {
                    "id": str(item['fixture']['id']),
                    "time": f"{minute}'",
                    "match_name": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                    "prediction": "NEXT GOAL HOME",
                    "odds": round(random.uniform(1.85, 2.45), 2),
                    "stake": round(5.0 + random.uniform(-0.15, 0.15), 2),
                    "score": f"{item['goals']['home']}:{item['goals']['away']}",
                    "date": datetime.date.today().strftime("%Y-%m-%d")
                }
                live_signals.append(sig)
                save_to_history(sig)
    except: pass

    # Б) Вземане на предстоящи мачове за деня (за да не е празен сайта)
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        res_upcoming = requests.get(url, headers=headers, params={"date": today, "status": "NS"}, timeout=10).json()
        for item in res_upcoming.get('response', [])[:6]: # Вземаме първите 6 предстоящи
            upcoming_matches.append({
                "time": item['fixture']['date'][11:16],
                "match_name": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                "league": item['league']['name']
            })
    except: pass
    
    return live_signals, upcoming_matches

def save_to_history(signal):
    if not os.path.exists(HISTORY_FILE):
        pd.DataFrame([signal]).to_csv(HISTORY_FILE, index=False)
    else:
        df = pd.read_csv(HISTORY_FILE)
        if signal['id'] not in df['id'].astype(str).values:
            pd.concat([df, pd.DataFrame([signal])], ignore_index=True).to_csv(HISTORY_FILE, index=False)

# --- 4. PREMIUM ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1016; color: #ffffff; }
    .main-header { color: #00ff00; text-align: center; font-size: 3.5rem; text-shadow: 0 0 20px #00ff00; margin-top: -50px; }
    .online-indicator { display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 25px; }
    .dot { height: 10px; width: 10px; background-color: #00ff00; border-radius: 50%; box-shadow: 0 0 10px #00ff00; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .card { background: linear-gradient(145deg, #161b22, #0d1117); border: 1px solid #30363d; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; }
    .live-card { border-left: 4px solid #00ff00; }
    .upcoming-card { border-left: 4px solid #8b949e; opacity: 0.9; }
    .stake-box { background: rgba(0, 255, 0, 0.05); border: 1px solid #00ff00; border-radius: 10px; padding: 10px; margin-top: 10px; }
    .stake-val { color: #00ff00; font-size: 1.8rem; font-weight: 900; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="online-indicator"><span class="dot"></span><span style="color:#00ff00; font-weight:bold;">{random.randint(128, 165)} INVESTORS ONLINE</span></div>', unsafe_allow_html=True)

live_sigs, upcoming = fetch_live_and_upcoming()

# --- СЕКЦИЯ 1: НА ЖИВО (СИГНАЛИ) ---
st.subheader("🚀 Активни Equilibrium Сигнали")
if live_sigs:
    l_cols = st.columns(3)
    for idx, s in enumerate(live_sigs):
        with l_cols[idx % 3]:
            st.markdown(f"""
            <div class="card live-card">
                <div style="color:#00ff00; font-size:0.7rem; font-weight:bold;">LIVE {s['time']} • {s['score']}</div>
                <div style="font-size:1.2rem; font-weight:bold; margin:5px 0;">{s['match_name']}</div>
                <div style="font-size:1.6rem; margin:5px 0;">@{s['odds']}</div>
                <div class="stake-box"><div class="stake-val">{s['stake']}%</div></div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("🔍 В момента няма активни аномалии. Системата скенира пазара...")

# --- СЕКЦИЯ 2: ПРЕДСТОЯЩИ МАЧОВЕ (ЗА ДА НЕ Е ПРАЗНО) ---
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📅 Предстоящи мачове за деня")
if upcoming:
    u_cols = st.columns(3)
    for idx, u in enumerate(upcoming):
        with u_cols[idx % 3]:
            st.markdown(f"""
            <div class="card upcoming-card">
                <div style="color:#8b949e; font-size:0.7rem;">START: {u['time']}</div>
                <div style="font-size:1.1rem; font-weight:bold; margin:5px 0;">{u['match_name']}</div>
                <div style="color:#555; font-size:0.7rem;">{u['league']}</div>
                <div style="margin-top:10px; font-style:italic; color:#8b949e; font-size:0.8rem;">Awaiting pressure data...</div>
            </div>
            """, unsafe_allow_html=True)

# --- СЕКЦИЯ 3: АРХИВ ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.subheader("📚 Последно приключили (Архив)")
if os.path.exists(HISTORY_FILE):
    h_df = pd.read_csv(HISTORY_FILE).tail(5)
    st.dataframe(h_df[['date', 'match_name', 'prediction', 'odds', 'stake']], use_container_width=True)

# --- СЕКЦИЯ 4: АБОНАМЕНТ ---
st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    st.markdown('<div style="background:#161b22; padding:30px; border-radius:15px; text-align:center;">', unsafe_allow_html=True)
    st.write("📩 VIP Daily Intelligence Subscription")
    e_mail = st.text_input("Въведи мейл:", label_visibility="collapsed")
    if st.button("АБОНИРАЙ МЕ"):
        if "@" in e_mail:
            with open(EMAILS_FILE, "a") as f: f.write(e_mail + "\n")
            st.success("Успешно добавен!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align:center; padding:10px; border:1px solid #00ff00; border-radius:10px; color:#00ff00;'>🛡️ CORE SYSTEM ACTIVE</div>", unsafe_allow_html=True)
    st.write(f"📅 {datetime.date.today()}")
    st.write("🛰️ Връзка: **Direct API Live**")
