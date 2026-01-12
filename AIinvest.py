import streamlit as st
import subprocess
import os
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# --- 1. АВТОМАТИЗАЦИЯ И СТАРТИРАНЕ НА ФОНОВИТЕ ПРОЦЕСИ ---
# Този блок гарантира, че collector.py (Equilibrium Engine) и mailer.py работят денонощно
if "processes_started" not in st.session_state:
    if os.path.exists("collector.py"):
        subprocess.Popen(["python", "collector.py"])
    if os.path.exists("mailer.py"):
        subprocess.Popen(["python", "mailer.py"])
    st.session_state["processes_started"] = True

# --- 2. ГЛОБАЛНИ НАСТРОЙКИ НА СТРАНИЦАТА ---
st.set_page_config(
    page_title="EQUILIBRIUM AI | Premium Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Автоматично опресняване на интерфейса на всеки 30 секунди
st_autorefresh(interval=30000, key="global_refresh")

# --- 3. PREMIUM DARK ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    /* Основен фон и шрифтове */
    .stApp {
        background-color: #0b0e14;
        color: #ffffff;
    }
    
    /* Заглавие с неон ефект */
    .main-header {
        color: #00ff00;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 3.5rem;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
        margin-top: -40px;
    }

    /* Карта на мача - Equilibrium Style */
    .eq-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 255, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .eq-card:hover {
        transform: translateY(-5px);
        border-color: #ffffff;
    }

    .match-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #ffffff;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .prediction-label {
        color: #00ff00;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.9rem;
    }

    /* Секция за залог с маскировка */
    .stake-container {
        background: rgba(0, 255, 0, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
    }

    .stake-amount {
        color: #00ff00;
        font-size: 2.2rem;
        font-weight: 900;
    }

    .status-text {
        font-size: 0.75rem;
        color: #8b949e;
        margin-top: 10px;
    }

    /* Секция Абонамент */
    .sub-box {
        background: #1e252e;
        padding: 40px;
        border-radius: 20px;
        border: 1px dashed #00ff00;
        text-align: center;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. СТРАНИЧНА ЛЕНТА (SETTINGS & API) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1683/1683828.png", width=80)
    st.title("Control Center")
    st.markdown("---")
    
    # Поле за API Ключ - Записва се автоматично за collector.py
    api_key_input = st.text_input("🔑 API-Football Key:", type="password", placeholder="Въведи RapidAPI ключ...")
    if api_key_input:
        with open("api_key.txt", "w") as f:
            f.write(api_key_input)
        st.success("API Ключът е внедрен!")

    st.markdown("---")
    st.write("🛰️ **Статус на системата:**")
    st.write("● Equilibrium Engine: **ACTIVE**")
    st.write("● Anti-Limit Masking: **ON**")
    
    if st.button("🚀 ПУСНИ ИМЕЙЛИ СЕГА"):
        subprocess.Popen(["python", "mailer.py", "--force"])
        st.toast("Сигналът за разпращане е изпратен успешно!")

# --- 5. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e; margin-bottom: 40px;'>Анализ на пазарни аномалии и математическо равновесие в реално време</p>", unsafe_allow_html=True)

# Зареждане на данните от Equilibrium Модела
data_file = "live_matches.csv"

if os.path.exists(data_file):
    try:
        df = pd.read_csv(data_file)
        
        # Проверка за съществуващи колони, за да няма червени грешки
        required_cols = ['match_name', 'prediction', 'odds', 'stake']
        if all(col in df.columns for col in required_cols) and not df.empty:
            
            # Създаване на решетка от 3 колони за картите
            display_cols = st.columns(3)
            
            for index, row in df.iterrows():
                with display_cols[index % 3]:
                    st.markdown(f"""
                    <div class="eq-card">
                        <div class="match-title">⚽ {row['match_name']}</div>
                        <div class="prediction-label">{row['prediction']}</div>
                        <div style="margin: 15px 0;">
                            <span style="font-size: 1.5rem; font-weight: bold;">@{row['odds']}</span>
                        </div>
                        <div class="stake-container">
                            <div style="color: #8b949e; font-size: 0.8rem; margin-bottom: 5px;">ПРЕПОРЪЧИТЕЛЕН ЗАЛОГ</div>
                            <div class="stake-amount">{row['stake']}%</div>
                        </div>
                        <div class="status-text">{row.get('status', 'Analyzing market gap...')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("⌛ Моделът изчислява пропастта в равновесието (Equilibrium Gap). Моля, изчакайте...")
    except Exception as e:
        st.error("Възникна грешка при синхронизацията на данните.")
else:
    st.warning("⚠️ Свързване с Equilibrium Engine... Прогнозите ще се заредят след миг.")

# --- 6. СЕКЦИЯ ЗА АБОНАМЕНТ (БАЗА ДАННИ С ИМЕЙЛИ) ---
st.markdown('<div class="sub-box">', unsafe_allow_html=True)
st.subheader("📩 VIP Имейл Известия")
st.write("Абонирайте се за ежедневния Equilibrium бюлетин (изпраща се точно в 10:00).")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    sub_email = st.text_input("Въведете вашия имейл:", placeholder="user@example.com", label_visibility="collapsed")
    if st.button("АБОНИРАЙ МЕ ЗА VIP СИГНАЛИ", use_container_width=True):
        if sub_email and "@" in sub_email:
            with open("emails.txt", "a") as f:
                f.write(sub_email + "\n")
            st.success(f"✅ Имейлът {sub_email} е добавен към базата данни!")
        else:
            st.error("Моля, въведете валиден имейл адрес.")
st.markdown('</div>', unsafe_allow_html=True)

# Футър
st.markdown("<br><hr><p style='text-align: center; color: #444; font-size: 0.8rem;'>EQUILIBRIUM AI v2.0 - Професионален софтуер за пазарен анализ</p>", unsafe_allow_html=True)
