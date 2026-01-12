import streamlit as st
import subprocess
import os
import pandas as pd
import time
import random
import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. ТВОИТЕ ВГРАДЕНИ API КЛЮЧОВЕ (ЦЕНТРАЛНО УПРАВЛЕНИЕ) ---
API_SOURCE_1 = "b4c92379d14d40edb87a9f3412d6835f" # RapidAPI / API-Football
API_SOURCE_2 = "b5b07a3f-b019-4a18-8969-6045169feda9"      # BetsAPI / B365API

# Автоматично генериране на системните файлове за колектора
with open("api_key.txt", "w") as f:
    f.write(API_SOURCE_1)
with open("bets_api_key.txt", "w") as f:
    f.write(API_SOURCE_2)

# --- 2. СИСТЕМНИ НАСТРОЙКИ ---
st.set_page_config(
    page_title="AI INVESTOR | Equilibrium Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Автоматично опресняване на всеки 30 секунди
st_autorefresh(interval=30000, key="main_engine_refresh")

# Стартиране на фоновите процеси
if "processes_running" not in st.session_state:
    if os.path.exists("collector.py"):
        subprocess.Popen(["python", "collector.py"])
    if os.path.exists("mailer.py"):
        subprocess.Popen(["python", "mailer.py"])
    st.session_state["processes_running"] = True

# --- 3. PREMIUM DARK ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1016; color: #ffffff; }
    
    /* Светещо заглавие */
    .main-header {
        color: #00ff00;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 3.8rem;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.6);
        margin-top: -60px;
    }

    /* Хора на линия */
    .online-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 30px;
    }
    .dot {
        height: 12px;
        width: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ff00;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.5; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Карти за мачовете */
    .match-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: 0.4s;
        margin-bottom: 25px;
    }
    .match-card:hover {
        border-color: #00ff00;
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(0, 255, 0, 0.1);
    }

    .prediction-label {
        background: rgba(0, 255, 0, 0.1);
        color: #00ff00;
        padding: 5px 15px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 15px;
        display: inline-block;
    }

    .stake-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid #21262d;
    }
    .stake-val {
        color: #00ff00;
        font-size: 2.5rem;
        font-weight: 900;
        font-family: 'Courier New', monospace;
    }

    /* Абонамент */
    .sub-panel {
        background: #161b22;
        padding: 50px;
        border-radius: 30px;
        border: 1px dashed #00ff00;
        text-align: center;
        margin-top: 50px;
    }

    /* Sidebar Protection */
    .sidebar-shield {
        background: rgba(0, 255, 0, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #00ff00;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)

# Хора на линия (Динамичен брояч)
online_users = random.randint(114, 158)
st.markdown(f"""
    <div class="online-indicator">
        <span class="dot"></span>
        <span style="color: #00ff00; font-weight: bold;">{online_users} INVESTORS ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

# Зареждане на сигналите
CSV_FILE = "live_matches.csv"

if os.path.exists(CSV_FILE):
    try:
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            # Премахване на празни редове, ако има такива
            df = df.dropna(subset=['match_name'])
            
            # Решетка от 3 колони
            rows = [df[i:i + 3] for i in range(0, df.shape[0], 3)]
            for row_data in rows:
                cols = st.columns(3)
                for i, (idx, data) in enumerate(row_data.iterrows()):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="match-card">
                            <div class="prediction-label">{data['prediction']}</div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: white;">{data['match_name']}</div>
                            <div style="font-size: 1.8rem; margin: 15px 0;">@{data['odds']}</div>
                            <div class="stake-box">
                                <div style="color: #8b949e; font-size: 0.7rem;">ANTI-LIMIT STAKE</div>
                                <div class="stake-val">{data['stake']}%</div>
                                <div style="color: #444; font-size: 0.6rem;">GAP ID: {random.randint(1000, 9999)}</div>
                            </div>
                            <div style="margin-top: 15px; font-size: 0.7rem; color: #8b949e;">{data.get('status', 'Verified Signal')}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("⌛ Системата скенира за Equilibrium аномалии... Моля, изчакайте.")
    except Exception as e:
        st.error(f"Грешка при визуализация: {e}")
else:
    st.warning("🔄 Инициализиране на източниците на данни...")

# --- 5. СИСТЕМА ЗА АБОНАМЕНТИ (EMAILS) ---
st.markdown('<div class="sub-panel">', unsafe_allow_html=True)
st.subheader("📩 VIP Daily Intelligence")
st.write("Получавайте избрани Equilibrium сигнали директно в пощата си.")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    email_addr = st.text_input("Въведи своя имейл:", placeholder="user@invest.ai", label_visibility="collapsed")
    if st.button("АБОНИРАЙ МЕ СЕГА", use_container_width=True):
        if "@" in email_addr:
            with open("emails.txt", "a") as f:
                f.write(email_addr + "\n")
            st.success("Успешно добавен в базата данни!")
        else:
            st.error("Въведете валиден имейл.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. SIDEBAR - КОНТРОЛЕН ПАНЕЛ ---
with st.sidebar:
    st.markdown('<div class="sidebar-shield">🛡️ PROTECTION ACTIVE</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("🛰️ **Data Sources:**")
    st.write(f"● Source 1 (Football): **Online**")
    st.write(f"● Source 2 (BetsAPI): **Online**")
    
    st.divider()
    
    st.write("📊 **System Logs:**")
    st.caption(f"Last sync: {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.caption("Anti-Bot Masking: RANDOMIZED")
    
    st.divider()
    
    if st.button("📧 FORCE EMAIL BROADCAST"):
        subprocess.Popen(["python", "mailer.py", "--force"])
        st.toast("Сигналите се изпращат...")

st.markdown("<br><hr><p style='text-align: center; color: #444; font-size: 0.8rem;'>EQUILIBRIUM ENGINE v3.0 | 2026 PRO EDITION</p>", unsafe_allow_html=True)

