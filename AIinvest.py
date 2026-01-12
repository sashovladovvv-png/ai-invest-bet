import streamlit as st
import subprocess
import threading
import os
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. АВТОМАТИЗАЦИЯ НА ПРОЦЕСИТЕ ---
def start_background_tasks():
    if "tasks_initialized" not in st.session_state:
        # Проверка и стартиране на Колектора
        if os.path.exists("collector.py"):
            subprocess.Popen(["python", "collector.py"])
        # Проверка и стартиране на Мейлъра
        if os.path.exists("mailer.py"):
            subprocess.Popen(["python", "mailer.py"])
        st.session_state["tasks_initialized"] = True

start_background_tasks()

# --- 2. НАСТРОЙКИ НА СТРАНИЦАТА ---
st.set_page_config(
    page_title="AI INVESTOR - Premium Signals",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Автоматично обновяване на всеки 30 секунди
st_autorefresh(interval=30000, key="data_update_refresh")

# --- 3. ЦЯЛОСТЕН ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .main-title {
        color: #00ff00;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 3.5rem;
        text-shadow: 0 0 25px #00ff00;
        margin-top: -50px;
    }
    .match-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 255, 0, 0.15);
        text-align: center;
    }
    .team-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    .prediction-text { color: #ffffff; font-size: 1.1rem; margin: 10px 0; }
    .odds-badge {
        background: #00ff00;
        color: #000;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .stake-container {
        margin-top: 20px;
        padding: 10px;
        background: rgba(0, 255, 0, 0.05);
        border-radius: 10px;
    }
    .stake-label { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }
    .stake-value { color: #00ff00; font-size: 2rem; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 AI INVESTOR</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Невронна мрежа за анализ на спортни събития в реално време</p>", unsafe_allow_html=True)

# --- 4. ЛОГИКА ЗА ДАННИТЕ ---
file_path = "live_matches.csv"

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Проверка на задължителни колони
        cols_needed = ['match_name', 'prediction', 'odds', 'stake']
        if all(c in df.columns for c in cols_needed) and not df.empty:
            layout_cols = st.columns(3)
            for idx, row in df.iterrows():
                with layout_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="match-card">
                        <div class="team-header">⚽ {row['match_name']}</div>
                        <div class="prediction-text">Прогноза: <b>{row['prediction']}</b></div>
                        <div style="margin: 15px 0;"><span class="odds-badge">@{row['odds']}</span></div>
                        <div class="stake-container">
                            <div class="stake-label">Препоръчителен залог</div>
                            <div class="stake-value">{row['stake']}%</div>
                            <div style="color: #444; font-size: 0.7rem;">ОТ ТЕКУЩАТА БАНКА</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("⌛ Системата в момента калибрира нови сигнали. Моля, изчакайте...")
    except Exception as e:
        st.error(f"Грешка при четене на базата данни. Опитайте обновяване.")
else:
    st.warning("⚠️ Базата данни се изгражда в момента от AI колектора. Моля, изчакайте 15-30 секунди...")

# Странично меню
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1683/1683828.png", width=100)
    st.title("Control Panel")
    st.write("Статус: **АКТИВЕН**")
    if st.button("📧 ИЗПРАТИ МЕЙЛИ СЕГА"):
        subprocess.Popen(["python", "mailer.py", "--force"])
        st.success("Сигналът за разпращане е подаден!")
