import streamlit as st
import requests
import datetime
import pytz

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | HYBRID ENGINE", layout="wide")

# КЛЮЧ 1: RapidAPI (за играчи - от снимка 71f51273)
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_HOST = "free-api-live-football-data.p.rapidapi.com"

# КЛЮЧ 2: iSports API (за мачове - от снимка c248d961)
# ЗАМЕНИ "ТУК_СЛОЖИ_ISPORTS_KEY" С ТВОЯ КЛЮЧ ОТ ISPORTS
ISPORTS_KEY = "ТУК_СЛОЖИ_ISPORTS_KEY" 

# --- 2. ДИЗАЙН ---
st.markdown("""
<style>
    .stApp { background-color: #05080a; color: white; }
    .match-box { background: #161b22; padding: 15px; border-radius: 8px; border-left: 5px solid #00ff00; margin-bottom: 10px; }
    .player-box { background: #0d1117; padding: 10px; border: 1px solid #30363d; border-radius: 5px; margin-top: 5px; }
    .highlight { color: #00ff00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 EQUILIBRIUM HYBRID: MATCH & PLAYER SCANNER")

# --- 3. ФУНКЦИИ ЗА ДАННИ ---

def get_isports_livescores():
    """Тегли мачове на живо от iSports API (Снимка c248d961)"""
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={ISPORTS_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    except:
        return []

def get_player_stats(player_name):
    """Тегли форма на играчи от RapidAPI (Снимка ccddc216)"""
    url = f"https://{RAPID_HOST}/football-get-search-players"
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_HOST}
    params = {"search_player": player_name}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        return res.json().get('response', [])
    except:
        return []

# --- 4. ОСНОВЕН ИНТЕРФЕЙС ---

tab1, tab2 = st.tabs(["📊 Мачове на живо (iSports)", "👤 Сканер за играчи (RapidAPI)"])

with tab1:
    st.subheader("Текущи събития от iSports API")
    if ISPORTS_KEY == "ТУК_СЛОЖИ_ISPORTS_KEY":
        st.warning("Моля, въведи своя iSports API ключ в кода.")
    else:
        livescores = get_isports_livescores()
        if livescores:
            for match in livescores[:15]:
                with st.container():
                    st.markdown(f"""
                    <div class="match-box">
                        <b>{match.get('homeName')} {match.get('homeScore')} - {match.get('awayScore')} {match.get('awayName')}</b><br>
                        <small>Лига: {match.get('leagueName')} | Статус: <span class="highlight">{match.get('status')}</span></small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Няма активни мачове в момента или ключът не е активиран.")

with tab2:
    st.subheader("Анализ на формата (Rapid Engine)")
    p_name = st.text_input("Въведи име на играч (на латиница):", "")
    if p_name:
        players = get_player_stats(p_name)
        if players:
            for p in players:
                st.markdown(f"""
                <div class="player-box">
                    <b>{p.get('name')}</b> ({p.get('team')})<br>
                    Рейтинг: <span class="highlight">{p.get('rating', 'N/A')}</span> | 
                    Голове: {p.get('goals', '0')} | Асистенции: {p.get('assists', '0')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Играчът не е намерен.")

# --- СТАТИСТИКА В СТРАНИЧНАТА ЛЕНТА ---
st.sidebar.image("https://img.icons8.com/neon/96/football.png")
st.sidebar.markdown(f"""
**Активни системи:**
- ✅ Player API: Active
- {'✅ Match API: Active' if ISPORTS_KEY != "ТУК_СЛОЖИ_ISPORTS_KEY" else '❌ Match API: Offline'}
""")
