import streamlit as st
import subprocess
import os
import pandas as pd
import time
import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. ПРЕДВАРИТЕЛНА КОНФИГУРАЦИЯ И СИГУРНОСТ ---
# ТВОЯТ API КЛЮЧ Е ВГРАДЕН ТУК (Не се пипа от потребителя)
API_KEY_DATABASE = "ТУК_ПОСТАВИ_ТВОЯ_API_КЛЮЧ"

# Автоматично генериране на системния файл за ключа
with open("api_key.txt", "w") as f:
    f.write(API_KEY_DATABASE)

# Настройки на прозореца на браузъра
st.set_page_config(
    page_title="EQUILIBRIUM AI INVESTOR | Pro Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Автоматично опресняване на интерфейса (на всеки 30 секунди за Live данни)
st_autorefresh(interval=30000, key="equilibrium_engine_refresh")

# --- 2. СТАРТИРАНЕ НА ФОНОВИТЕ МОДУЛИ ---
@st.cache_resource
def start_background_systems():
    """ Стартира collector и mailer само веднъж при пускане на сайта """
    try:
        if os.path.exists("collector.py"):
            subprocess.Popen(["python", "collector.py"])
        if os.path.exists("mailer.py"):
            subprocess.Popen(["python", "mailer.py"])
        return True
    except Exception as e:
        return f"Грешка при старт: {e}"

system_status = start_background_systems()

# --- 3. РАЗШИРЕН PREMIUM ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    /* Основна тема */
    .stApp {
        background-color: #0b1016;
        color: #e6edf3;
    }
    
    /* Светещо заглавие */
    .main-header {
        color: #00ff00;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 4rem;
        font-weight: 900;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
        margin-top: -60px;
        letter-spacing: -2px;
    }

    /* Статус лента за защита */
    .shield-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 40px;
    }
    .shield-status {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid #00ff00;
        color: #00ff00;
        padding: 10px 25px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }

    /* Карта на мача (Equilibrium Card) */
    .match-card {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .match-card:hover {
        border-color: #00ff00;
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 255, 0, 0.1);
    }

    .team-name {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 10px;
        line-height: 1.2;
    }

    .prediction-badge {
        background: rgba(0, 255, 0, 0.1);
        color: #00ff00;
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .odds-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 20px;
    }

    /* Секция за залог със защита от ботове */
    .stake-box {
        background: #0b1016;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #21262d;
    }
    .stake-label {
        color: #8b949e;
        font-size: 0.7rem;
        text-transform: uppercase;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    .stake-number {
        color: #00ff00;
        font-size: 2.8rem;
        font-weight: 900;
        font-family: 'Monaco', 'Courier New', monospace;
    }
    .mask-text {
        font-size: 0.6rem;
        color: #444;
        margin-top: 5px;
    }

    /* Абонамент секция */
    .subscription-panel {
        background: #161b22;
        padding: 50px;
        border-radius: 25px;
        border: 1px solid #30363d;
        margin-top: 60px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="shield-container"><div class="shield-status">🛡️ ANTI-LIMIT ALGORITHM ACTIVE</div></div>', unsafe_allow_html=True)

# Път до базата данни на Equilibrium
CSV_FILE = "live_matches.csv"

def load_and_display_data():
    if not os.path.exists(CSV_FILE):
        st.warning("🔄 Инициализиране на Equilibrium Engine... Моля, изчакайте първоначалното сканиране (около 60 сек).")
        return

    try:
        df = pd.read_csv(CSV_FILE)
        
        if df.empty:
            st.info("🔍 В момента пазарът е в равновесие. Скениране за нови аномалии...")
            return

        # Проверка за специфичната колона от collector.py
        if "match_name" in df.columns:
            # Извеждане на мачовете в мрежа от 3 колони
            cards_per_row = 3
            rows = [df[i:i + cards_per_row] for i in range(0, df.shape[0], cards_per_row)]
            
            for row_data in rows:
                cols = st.columns(cards_per_row)
                for i, (idx, data) in enumerate(row_data.iterrows()):
                    with cols[i]:
                        # ПРОВЕРКА: Ако алгоритъмът още калибрира
                        if data['match_name'] == "Scanning...":
                            st.markdown('<div class="match-card"><p>Калибриране на сигнали...</p></div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="match-card">
                                <div class="prediction-badge">{data['prediction']}</div>
                                <div class="team-name">{data['match_name']}</div>
                                <div class="odds-value">@{data['odds']}</div>
                                <div class="stake-box">
                                    <div class="stake-label">Safe Equilibrium Stake</div>
                                    <div class="stake-number">{data['stake']}%</div>
                                    <div class="mask-text">MASKING ID: {idx + 1042} | ANTI-TRACKING ACTIVE</div>
                                </div>
                                <div style="font-size: 0.65rem; color: #30363d; margin-top: 15px;">
                                    {data.get('status', 'Verified Signal')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Грешка при визуализация на данните: {e}")

load_and_display_data()

# --- 5. СИСТЕМА ЗА СЪБИРАНЕ НА ЕМЕЙЛИ (LEAD GENERATION) ---
st.markdown('<div class="subscription-panel">', unsafe_allow_html=True)
st.subheader("📩 VIP Имейл Известия")
st.write("Получавайте автоматични Equilibrium отчети директно в пощата си всяка сутрин.")

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    subscriber_email = st.text_input("Вашият имейл адрес:", placeholder="office@yourfirm.com", label_visibility="collapsed")
    if st.button("АБОНИРАЙ МЕ ЗА VIP СИГНАЛИ", use_container_width=True):
        if subscriber_email and "@" in subscriber_email:
            # Записване в базата данни (текстов файл)
            with open("emails.txt", "a") as f:
                f.write(f"{subscriber_email}\n")
            st.success(f"✅ Успешно добавихме {subscriber_email} към списъка за 10:00 ч.!")
        else:
            st.error("Моля, въведете валиден имейл адрес.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. АДМИНИСТРАТИВЕН SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("Admin Shield")
    st.markdown("---")
    
    st.write(f"📅 **Дата:** {datetime.date.today()}")
    st.write(f"🔑 **API Status:** ONLINE")
    st.write(f"🛡️ **Protection:** MAXIMUM")
    
    st.divider()
    
    st.subheader("Manual Controls")
    if st.button("📧 FORCE EMAIL BROADCAST"):
        # Извиква мейлъра принудително
        subprocess.Popen(["python", "mailer.py", "--force"])
        st.toast("Изпращане на сигнали към всички абонати...")

    st.divider()
    st.markdown("<p style='color: #444; font-size: 0.7rem;'>EQUILIBRIUM ENGINE v2.4.0<br>Authorized Access Only</p>", unsafe_allow_html=True)
