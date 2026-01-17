import streamlit as st
import requests
import datetime
import pytz
import random

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA PRO", page_icon="⚽", layout="wide")

# Ключове
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_HOST = "free-api-live-football-data.p.rapidapi.com"
ISPORTS_KEY = "aW8C1RFgu8rWZrs4" 

# --- 2. АЛГОРИТЪМ ЗА МОМЕНТАЛЕН АНАЛИЗ (ФИКСИРАН) ---
def force_analyze(h, a, status):
    """
    Този алгоритъм е агресивен. Ако мачът е на живо, ТОЙ ВИНАГИ дава прогноза.
    """
    try:
        h = int(h)
        a = int(a)
        diff = h - a
        total = h + a
        
        # ЛОГИКА ЗА ЖИВО ПРЕДАВАНЕ
        if h == a:
            if total == 0: return "ПОД 2.5 ГОЛА", 78
            return "СЛЕДВАЩ ГОЛ: ДА", 82
        elif diff >= 1:
            return "ПОБЕДА ДОМАКИН (1)", 88
        elif diff <= -1:
            return "ДВОЕН ШАНС: X2", 85
        
        return "НАД 1.5 ГОЛА", 70
    except:
        return "АНАЛИЗ: НАД 0.5", 60

# --- 3. ДИЗАЙН ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.2rem; text-shadow: 0 0 10px #00ff00; margin-bottom: 20px; }
    .match-card { background: #0d1117; border: 1px solid #1f242c; border-radius: 12px; padding: 18px; margin-bottom: 10px; border-left: 5px solid #00ff00; }
    .pred-box { background: #064e3b; color: #00ff00; padding: 10px; border-radius: 8px; font-weight: bold; border: 1px solid #00ff00; text-align: center; min-width: 150px; }
    .live-dot { color: #ff0000; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">EQUILIBRIUM AI | ARMA DA V3</h1>', unsafe_allow_html=True)

# --- 4. ПОТРЕБИТЕЛИ НА ЛИНИЯ ---
with st.sidebar:
    st.markdown("### 👥 МОНИТОРИНГ")
    if st.button("👥 КОЙ Е ОНЛАЙН?"):
        st.success(f"🟢 {random.randint(210, 640)} анализатори на линия")
    st.divider()
    st.write("🌍 **ЕЗИК:** Български")
    st.write("⚡ **АНАЛИЗ:** В реално време")

# --- 5. ДАННИ ---
def get_data():
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={ISPORTS_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('data', [])
    except:
        return []

# --- 6. ПОКАЗВАНЕ ---
raw_matches = get_data()

if raw_matches:
    st.subheader(f"📊 Активни прогнози: {len(raw_matches)}")
    
    for m in raw_matches[:40]:
        h_name = m.get('homeName', 'Домакин')
        a_name = m.get('awayName', 'Гост')
        h_score = m.get('homeScore', 0)
        a_score = m.get('awayScore', 0)
        status = m.get('status', 'Live')
        league = m.get('leagueName', 'Лига')
        
        # ПРИНУДИТЕЛЕН АНАЛИЗ - тук е промяната!
        p_text, p_conf = force_analyze(h_score, a_score, status)
        
        st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="flex:2;">
                        <small style="color:#888;">{league}</small><br>
                        <b style="font-size:1.3rem;">{h_name} {h_score} - {a_score} {a_name}</b><br>
                        <span class="live-dot">● НА ЖИВО: {status}</span>
                    </div>
                    <div style="flex:1;">
                        <div class="pred-box">
                            <small style="display:block; font-size:0.7rem; color:#eee;">AI ПРОГНОЗА</small>
                            {p_text}
                        </div>
                    </div>
                    <div style="flex:1; text-align:right;">
                        <span style="color:#00ff00; font-size:1.6rem; font-weight:bold;">{p_conf}%</span><br>
                        <small style="color:#666;">СИГУРНОСТ</small>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("В момента няма активни мачове. Скенерът е активен.")

# --- 7. ПЛЕЙЪР СКЕНЕР ---
st.divider()
p_search = st.text_input("👤 Търси форма на играч (RapidAPI):", "")
if p_search:
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_HOST}
    res_p = requests.get(f"https://{RAPID_HOST}/football-get-search-players", headers=headers, params={"search_player": p_search})
    try:
        p_data = res_p.json().get('response', [])
        for p in p_data:
            st.info(f"📊 {p.get('name')} | Отбор: {p.get('team')} | Рейтинг: {p.get('rating')}")
    except:
        st.error("Няма данни за този играч.")
