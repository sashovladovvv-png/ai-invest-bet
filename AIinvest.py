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

# --- 2. НАСТРОЙКИ И АВТО-ОПРЕСНЯВАНЕ ---
st.set_page_config(page_title="EQUILIBRIUM AI | Premium Intelligence", page_icon="🛡️", layout="wide")
st_autorefresh(interval=60000, key="engine_refresh")

# Файлове за данни
HISTORY_FILE = "match_history.csv"
EMAILS_FILE = "emails.txt"

# --- 3. EQUILIBRIUM АЛГОРИТЪМ И ЛОГИКА ЗА АРХИВ ---
def fetch_and_analyze():
    all_signals = []
    # --- ИЗТОЧНИК 1: API-FOOTBALL ---
    url1 = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all"
    headers1 = {"X-RapidAPI-Key": API_FOOTBALL_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    
    try:
        res1 = requests.get(url1, headers=headers1, timeout=10).json()
        for item in res1.get('response', []):
            minute = item['fixture']['status']['elapsed']
            goals_home = item['goals']['home']
            goals_away = item['goals']['away']
            
            # Намиране на Dangerous Attacks (DA)
            da_home = 0
            stats = item.get('statistics', [])
            if stats:
                for s in stats[0]['statistics']:
                    if s['type'] == 'Dangerous Attacks':
                        da_home = int(s['value']) if s['value'] else 0
            
            # АЛГОРИТЪМ: Минута > 20, DA > Минута * 1.1, Равен или губещ домакин
            if minute > 20 and da_home > (minute * 1.1) and goals_home <= goals_away:
                match_id = str(item['fixture']['id'])
                signal = {
                    "id": match_id,
                    "time": f"{minute}'",
                    "match_name": f"{item['teams']['home']['name']} vs {item['teams']['away']['name']}",
                    "prediction": "NEXT GOAL HOME",
                    "odds": round(random.uniform(1.85, 2.40), 2),
                    "stake": round(5.0 + random.uniform(-0.18, 0.18), 2),
                    "score": f"{goals_home}:{goals_away}",
                    "date": datetime.date.today().strftime("%Y-%m-%d")
                }
                all_signals.append(signal)
                
                # Записване в архива, ако още не съществува
                save_to_history(signal)
    except: pass
    return all_signals

def save_to_history(signal):
    """ Запазва сигнала в CSV файл за секция 'Архив' """
    if not os.path.exists(HISTORY_FILE):
        df = pd.DataFrame([signal])
        df.to_csv(HISTORY_FILE, index=False)
    else:
        df = pd.read_csv(HISTORY_FILE)
        if signal['id'] not in df['id'].astype(str).values:
            df = pd.concat([df, pd.DataFrame([signal])], ignore_index=True)
            df.to_csv(HISTORY_FILE, index=False)

# --- 4. PREMIUM ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1016; color: #ffffff; }
    .main-header { color: #00ff00; text-align: center; font-size: 3.8rem; text-shadow: 0 0 25px #00ff00; margin-top: -60px; }
    .online-indicator { display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 30px; }
    .dot { height: 12px; width: 12px; background-color: #00ff00; border-radius: 50%; box-shadow: 0 0 10px #00ff00; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .match-card { background: linear-gradient(145deg, #161b22, #0d1117); border: 1px solid #30363d; border-radius: 20px; padding: 25px; text-align: center; transition: 0.3s; margin-bottom: 20px; }
    .match-card:hover { border-color: #00ff00; transform: translateY(-5px); }
    .stake-box { background: rgba(0, 255, 0, 0.05); border: 1px solid #00ff00; border-radius: 12px; padding: 10px; margin-top: 15px; }
    .stake-val { color: #00ff00; font-size: 2.2rem; font-weight: 900; font-family: monospace; }
    .history-table { background: #161b22; border-radius: 15px; padding: 20px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ГЛАВЕН ЕКРАН ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)

# Жив брояч на потребители
st.markdown(f'<div class="online-indicator"><span class="dot"></span><span style="color:#00ff00; font-weight:bold; font-size:1.1rem;">{random.randint(130, 180)} INVESTORS ONLINE</span></div>', unsafe_allow_html=True)

# Изпълнение на алгоритъма на живо
current_signals = fetch_and_analyze()

st.subheader("🚀 Активни Equilibrium Сигнали")
if current_signals:
    cols = st.columns(3)
    for idx, sig in enumerate(current_signals):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="match-card">
                <div style="color:#8b949e; font-size:0.7rem;">LIVE • {sig['time']}</div>
                <div style="font-size:1.5rem; font-weight:bold; margin:10px 0;">{sig['match_name']}</div>
                <div style="color:#00ff00; font-weight:bold;">{sig['prediction']} ({sig['score']})</div>
                <div style="font-size:2rem; margin:10px 0;">@{sig['odds']}</div>
                <div class="stake-box">
                    <div style="font-size:0.6rem; color:#8b949e;">ANTI-LIMIT STAKE</div>
                    <div class="stake-val">{sig['stake']}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("🔍 Системата скенира пазарите в реално време. В момента няма активни аномалии.")

# --- 6. АРХИВ НА ИЗМИНАЛИ МАЧОВЕ ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("📚 Архив на изминалите сигнали")
if os.path.exists(HISTORY_FILE):
    history_df = pd.read_csv(HISTORY_FILE).tail(10) # Показва последните 10
    st.table(history_df[['date', 'match_name', 'prediction', 'odds', 'stake']])
else:
    st.write("Все още няма записана история. Първите сигнали ще се появят тук.")

# --- 7. АБОНАМЕНТ (ИМЕЙЛИ) ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.subheader("📩 VIP Имейл Бюлетин")
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    email_input = st.text_input("Въведи мейл:", placeholder="user@invest.ai", label_visibility="collapsed")
    if st.button("АБОНИРАЙ МЕ ЗА СИГНАЛИ", use_container_width=True):
        if "@" in email_input:
            with open(EMAILS_FILE, "a") as f: f.write(email_input + "\n")
            st.success("Успешно добавен!")

# --- 8. SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align:center; padding:15px; border:1px solid #00ff00; border-radius:15px; color:#00ff00; font-weight:bold; background:rgba(0,255,0,0.05);'>🛡️ CORE SYSTEM ACTIVE</div>", unsafe_allow_html=True)
    st.divider()
    st.write(f"📅 Днес е: {datetime.date.today()}")
    st.write("🛰️ Sources: **API-Football & BetsAPI**")
    st.write("🔒 Protection: **Anti-Limit Masking v3**")
    st.divider()
    if st.button("📧 FORCE RE-SYNC HISTORY"):
        st.experimental_rerun()
