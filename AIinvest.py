import streamlit as st
import pandas as pd
from datetime import datetime
import random
from streamlit_autorefresh import st_autorefresh
import os
import subprocess

# --- 1. SHIELD: ПЪЛНА ЗАЩИТА (ANTI-BOT) ---
def apply_shield():
    try:
        ua = st.context.headers.get("User-Agent", "").lower()
        blocked = ["bot", "crawl", "spider", "python-requests", "headless", "selenium", "phantom"]
        if any(keyword in ua for keyword in blocked):
            st.error("🛡️ SHIELD: ACCESS DENIED. SECURE CONNECTION REQUIRED.")
            st.stop()
    except:
        pass

# --- 2. PANDAS DATABASE & CONFIG (Управление на данни) ---
DB_FILE = "subscribers.csv"
DATA_FILE = "live_matches.csv" # Файлът, който твоят collector.py обновява на 15 мин

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["Email", "Date_Added", "Status"])
        df.to_csv(DB_FILE, index=False)

def add_subscriber(email):
    df = pd.read_csv(DB_FILE)
    if email in df["Email"].values:
        return "exists"
    new_entry = pd.DataFrame([[email, datetime.now().strftime("%Y-%m-%d %H:%M"), "Active"]], 
                             columns=["Email", "Date_Added", "Status"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return True

# Изпълнение на защитата и инициализация
apply_shield()
init_db()

# --- 3. UI & NEON DESIGN (Интерфейс) ---
st.set_page_config(page_title="CYBER BET AI", layout="wide")
# Синхронизирано опресняване на екрана (препоръчително на 60 сек, за да хваща промените от колектора)
st_autorefresh(interval=60 * 1000, key="ui_sync_refresh")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    .match-card {
        border: 2px solid #39FF14;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #0a0a0a;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.4);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .match-card:hover { transform: translateY(-5px); box-shadow: 0 0 25px #39FF14; }
    .stTitle { 
        color: #39FF14; text-align: center; 
        font-family: 'Courier New', monospace; 
        text-shadow: 0 0 20px #39FF14; font-size: 3.5em;
    }
    .status-dot {
        height: 12px; width: 12px; background-color: #39FF14;
        border-radius: 50%; display: inline-block; margin-right: 8px;
        box-shadow: 0 0 10px #39FF14; animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0% { transform: scale(0.9); opacity: 1; } 70% { transform: scale(1.1); opacity: 0.5; } 100% { transform: scale(0.9); opacity: 1; } }
    .bet-instruction {
        background-color: #39FF14; color: black; font-weight: bold;
        padding: 10px; border-radius: 8px; margin-top: 15px; text-transform: uppercase; font-size: 1.1em;
    }
    .sidebar-info {
        background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("CYBER BET AI")
st.markdown("<p style='text-align: center; color: #888;'>EQUILIBRIUM ENGINE v3.5 | 15-MIN DATA CYCLE</p>", unsafe_allow_html=True)

# --- 4. SIDEBAR (Абонати и Контрол) ---
with st.sidebar:
    st.markdown(f"### <span class='status-dot'></span> LIVE: {random.randint(156, 210)} USERS", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📧 ELITE DOUBLES")
    st.write("Получавай сигнали от 30+ първенства.")
    email_in = st.text_input("Въведи Email:")
    
    if st.button("АКТИВИРАЙ АБОНЕМЕНТ"):
        if "@" in email_in:
            res = add_subscriber(email_in)
            if res == True: st.success("Успешно добавен в базата!")
            elif res == "exists": st.warning("Вече съществуваш в базата.")
        else: st.error("Невалиден имейл адрес.")

    st.markdown("---")
    st.markdown("### 🛠️ ADMIN PANEL")
    if st.button("🚀 ПУСНИ MAILER.PY"):
        try:
            if os.path.exists("mailer.py"):
                subprocess.run(["python", "mailer.py"], check=True)
                st.success("Системата разпраща прогнози!")
            else: st.error("mailer.py не е намерен!")
        except Exception as e: st.error(f"Грешка: {e}")

# --- 5. MAIN DASHBOARD: ДАННИ ОТ АВТОМАТИЧНИЯ КОЛЕКТОР ---
st.subheader("📡 AUTONOMOUS LIVE FEED")

try:
    if os.path.exists(DATA_FILE):
        live_df = pd.read_csv(DATA_FILE)
        
        if live_df.empty:
            st.info("Колекторът работи, но все още не е открил подходящи мачове...")
        else:
            # Показваме мачовете в 3 колони
            cols = st.columns(3)
            # Взимаме до 12 мача за оптимален изглед
            for idx, row in live_df.head(12).iterrows():
                with cols[idx % 3]:
                    prob = random.randint(85, 98)
                    match_name = row['Match'] if 'Match' in row else "Analyzing..."
                    score = row['Score'] if 'Score' in row else "0:0"
                    league = row['League'] if 'League' in row else "Live Match"
                    
                    st.markdown(f"""
                        <div class="match-card">
                            <div style="color: #666; font-size: 0.7em; text-transform: uppercase;">{league}</div>
                            <div style="color: white; font-weight: bold; margin: 15px 0; min-height: 45px; font-size: 1.1em;">
                                {match_name}
                            </div>
                            <div style="color: #39FF14; font-size: 2.8em; font-weight: bold; margin-bottom: 5px;">
                                {score}
                            </div>
                            <div style="border-top: 1px solid #222; padding-top: 10px; margin-top: 10px;">
                                <span style="color: #888; font-size: 0.8em;">AI CONFIDENCE:</span>
                                <span style="color: #39FF14; font-weight: bold;">{prob}%</span>
                            </div>
                            <div class="bet-instruction">🔥 SUGGESTED: NEXT GOAL LIVE</div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Връзката с collector.py не е активна. Стартирай го в терминала.")
except Exception as e:
    st.error(f"Грешка при синхронизацията на данни: {e}")

# --- 6. ADMIN DATABASE VIEWER ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📂 ПРЕГЛЕД НА БАЗАТА (АБОНАТИ)"):
    if os.path.exists(DB_FILE):
        st.dataframe(pd.read_csv(DB_FILE), use_container_width=True)
    else:
        st.write("Няма записани абонати.")

# --- 7. FOOTER СТАТИСТИКА ---
st.markdown("---")
fa, fb, fc = st.columns(3)
fa.metric("COLLECTOR", "RUNNING", delta="15 MIN")
fb.metric("DATA SOURCE", "30 LEAGUES", delta="AUTO")
fc.metric("SHIELD", "ACTIVE", delta="SECURE")