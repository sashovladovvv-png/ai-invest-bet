import streamlit as st
import subprocess
import os
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. ТВОЯТ API КЛЮЧ (ЗАКЛЮЧЕН В КОДА) ---
API_KEY = "b4c92379d14d40edb87a9f3412d6835f"

# Автоматично създаване на api_key.txt за работа на collector.py
with open("api_key.txt", "w") as f:
    f.write(API_KEY)

# --- 2. СТАРТИРАНЕ НА ЗАЩИТЕНИТЕ ПРОЦЕСИ ---
if "initialized" not in st.session_state:
    if os.path.exists("collector.py"):
        # Стартира collector.py, който съдържа "Anti-Limit" математиката
        subprocess.Popen(["python", "collector.py"])
    if os.path.exists("mailer.py"):
        subprocess.Popen(["python", "mailer.py"])
    st.session_state["initialized"] = True

# --- 3. НАСТРОЙКИ НА СТРАНИЦАТА ---
st.set_page_config(
    page_title="EQUILIBRIUM AI | Anti-Limit Protected",
    page_icon="🛡️",
    layout="wide"
)

st_autorefresh(interval=30000, key="secure_refresh")

# --- 4. ДИЗАЙН СЪС ЗАЩИТНИ ЕЛЕМЕНТИ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .main-title {
        color: #00ff00;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 3.2rem;
        text-shadow: 0 0 20px #00ff00;
    }
    .status-shield {
        text-align: center;
        color: #00ff00;
        font-size: 0.9rem;
        margin-bottom: 30px;
        border: 1px solid #00ff00;
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
        padding: 5px 15px;
        border-radius: 20px;
        background: rgba(0, 255, 0, 0.1);
    }
    .match-card {
        background: #161b22;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }
    .match-card:hover { border-color: #00ff00; box-shadow: 0 0 15px rgba(0,255,0,0.2); }
    .stake-value {
        color: #00ff00;
        font-size: 2.5rem;
        font-weight: 900;
        font-family: 'Courier New', monospace; /* Моноширинен шрифт за прецизност */
    }
    .protected-badge {
        font-size: 0.6rem;
        color: #8b949e;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="status-shield">🛡️ ANTI-LIMIT PROTECTION ACTIVE</div>', unsafe_allow_html=True)

# --- 5. ВИЗУАЛИЗАЦИЯ НА СИГНАЛИТЕ (EQUILIBRIUM DATA) ---
file_path = "live_matches.csv"

if os.path.exists(file_path):
    try:
        df = pd.read_csv(file_path)
        if not df.empty:
            cols = st.columns(3)
            for idx, row in df.iterrows():
                with cols[idx % 3]:
                    # Тук се визуализира "маскираният" залог от collector.py
                    st.markdown(f"""
                    <div class="match-card">
                        <div style="color:white; font-weight:bold; font-size:1.2rem;">{row['match_name']}</div>
                        <div style="color:#00ff00; margin-top:5px; font-size:0.8rem;">{row['prediction']}</div>
                        <div style="font-size:1.5rem; margin:15px 0;">@{row['odds']}</div>
                        <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px;">
                            <div class="protected-badge">SAFE STAKE MODEL</div>
                            <div class="stake-value">{row['stake']}%</div>
                        </div>
                        <div style="font-size:0.7rem; color:#444; margin-top:10px;">Gap ID: {row.get('status', 'Verified')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🔍 Системата анализира пазара за Equilibrium аномалии...")
    except:
        st.error("Грешка при синхронизация на данните.")
else:
    st.warning("🔄 Инициализиране на защитения модул...")

# --- 6. ГРАФА ЗА ИМЕЙЛИ (БАЗА ДАННИ) ---
st.markdown("<br><br><div style='text-align:center;'>", unsafe_allow_html=True)
st.subheader("📩 VIP Имейл Абонамент")
email = st.text_input("Въведи мейл за ежедневни отчети (10:00 ч.):", placeholder="example@mail.com")
if st.button("АБОНИРАЙ МЕ"):
    if "@" in email:
        with open("emails.txt", "a") as f:
            f.write(email + "\n")
        st.success("✅ Успешно добавен в защитения списък!")
st.markdown("</div>", unsafe_allow_html=True)

# --- 7. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Guard Panel")
    st.write("API: **Encrypted**")
    st.write("Masking: **Randomized**")
    st.divider()
    if st.button("📧 FORCE SEND MAIL"):
        subprocess.Popen(["python", "mailer.py", "--force"])
        st.toast("Изпращане...")
