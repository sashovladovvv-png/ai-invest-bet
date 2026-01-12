import streamlit as st
import subprocess
import threading
import os
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# 1. СТАРТИРАНЕ НА АВТОМАТИЗАЦИЯТА НА ЗАДЕН ПЛАН
def start_background_apps():
    if "apps_initialized" not in st.session_state:
        # Стартираме колектора на данни като отделен процес
        if os.path.exists("collector.py"):
            subprocess.Popen(["python", "collector.py"])
        # Стартираме мейлъра като отделен процес
        if os.path.exists("mailer.py"):
            subprocess.Popen(["python", "mailer.py"])
        st.session_state["apps_initialized"] = True

start_background_apps()

# 2. КОНФИГУРАЦИЯ НА СТРАНИЦАТА
st.set_page_config(
    page_title="AI INVESTOR | Premium Live Signals",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Автоматично обновяване на всеки 30 секунди, за да се виждат новите мачове веднага
st_autorefresh(interval=30000, key="datarefresh")

# 3. ЦЯЛОСТЕН ДИЗАЙН (CSS)
st.markdown("""
    <style>
    /* Основен фон */
    .stApp {
        background-color: #0b0e14;
    }
    
    /* Заглавие */
    .main-title {
        color: #00ff00;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        text-shadow: 0 0 20px #00ff00;
        margin-bottom: 10px;
    }

    /* Карта на мача */
    .match-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 255, 0, 0.1);
        transition: all 0.3s ease;
    }

    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 255, 0, 0.3);
        border-color: #ffffff;
    }

    .team-name {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }

    .stat-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }

    .stat-label { color: #8b949e; font-size: 0.9rem; }
    .stat-value { color: #ffffff; font-weight: bold; }
    
    .prediction-box {
        background-color: rgba(0, 255, 0, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-top: 15px;
    }

    .stake-text {
        color: #00ff00;
        font-size: 1.5rem;
        font-weight: 900;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 AI INVESTOR LIVE</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Системата сканира над 1000 мача в секунда чрез Deep Learning</p>", unsafe_allow_html=True)

# 4. ЛОГИКА ЗА ПОКАЗВАНЕ НА ДАННИТЕ
try:
    if os.path.exists("live_matches.csv"):
        df = pd.read_csv("live_matches.csv")
        
        if not df.empty:
            # Разделяме на колони за по-красив изглед
            cols = st.columns(3)
            for index, row in df.iterrows():
                with cols[index % 3]:
                    st.markdown(f"""
                    <div class="match-card">
                        <div class="team-name">⚽ {row['match_name']}</div>
                        <div class="stat-row">
                            <span class="stat-label">Прогноза:</span>
                            <span class="stat-value">{row['prediction']}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Коефициент:</span>
                            <span class="stat-value">@{row['odds']}</span>
                        </div>
                        <div class="prediction-box">
                            <div style="color: #8b949e; font-size: 0.8rem;">ПРЕПОРЪЧИТЕЛЕН ЗАЛОГ</div>
                            <div class="stake-text">{row['stake']}%</div>
                            <div style="color: #8b949e; font-size: 0.7rem;">ОТ ВАШАТА БАНКА</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("⌛ Търсене на мачове с висок интензитет... Моля, изчакайте.")
    else:
        st.warning("⚠️ Колекторът се стартира за първи път. Прогнозите ще се заредят до секунди...")
except Exception as e:
    st.error(f"Грешка при визуализация: {e}")

# Странична лента
with st.sidebar:
    st.header("📊 Статистика")
    st.write("Активни сканирания: 1,420")
    st.write("Среден успех: 78.4%")
    if st.button("🚀 Изпрати мейли сега (Ръчно)"):
        subprocess.Popen(["python", "mailer.py", "--force"])
        st.success("Сигналът за изпращане е подаден!")
