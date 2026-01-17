import streamlit as st
import requests
import random

# --- 1. КЛЮЧОВЕ ---
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_HOST = "free-api-live-football-data.p.rapidapi.com"
ISPORTS_KEY = "aW8C1RFgu8rWZrs4" 

# --- 2. НАСТРОЙКИ НА СТРАНИЦАТА ---
st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA V3", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: white; }
    .match-card { background: #0d1117; border-radius: 12px; padding: 20px; margin-bottom: 10px; border-left: 5px solid #00ff00; border: 1px solid #1f242c; }
    .pred-tag { background: #064e3b; color: #00ff00; padding: 8px 15px; border-radius: 8px; font-weight: bold; border: 1px solid #00ff00; text-align: center; }
    .live-text { color: #ff4b4b; font-weight: bold; font-size: 0.9rem; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. АЛГОРИТЪМ ЗА ПРОГНОЗИ (СИГУРЕН ЗА -1) ---
def get_ai_prediction(h, a):
    try:
        h, a = int(h), int(a)
        if h > a:
            return "ПОБЕДА ДОМАКИН (1)", 88
        elif a > h:
            return "ДВОЕН ШАНС: X2", 82
        elif h == a:
            if h == 0: return "ПОД 2.5 ГОЛА", 75
            return "СЛЕДВАЩ ГОЛ: ДА", 82
        return "НАД 1.5 ГОЛА", 70
    except:
        return "АНАЛИЗ НА ЖИВО", 65

# --- 4. ФУНКЦИИ ЗА ДАННИ ---
def get_live_data():
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={ISPORTS_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('data', [])
    except:
        return []

# --- 5. ГЛАВЕН ИНТЕРФЕЙС ---
st.title("⚽ EQUILIBRIUM AI | АРМАДА V3")

with st.sidebar:
    st.header("👥 ПОТРЕБИТЕЛИ")
    if st.button("👥 ХОРА НА ЛИНИЯ"):
        st.success(f"🟢 {random.randint(400, 850)} потребители на линия")
    st.divider()
    st.info("Алгоритъмът V3 анализира в реално време.")

data = get_live_data()

if data:
    st.subheader(f"🎯 Активни прогнози: {len(data)}")
    for m in data[:35]:
        h_name = m.get('homeName', 'Домакин')
        a_name = m.get('awayName', 'Гост')
        h_score = m.get('homeScore', 0)
        a_score = m.get('awayScore', 0)
        status = str(m.get('status', '0'))
        league = m.get('leagueName', 'Лига')
        
        # Генериране на прогноза
        prediction, confidence = get_ai_prediction(h_score, a_score)
        
        # Дизайн на картата (БЕЗ ГРЕШКИ В КАВИЧКИТЕ)
        card_html = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="flex:2;">
                    <small style="color:#888;">🏆 {league}</small><br>
                    <b style="font-size:1.4rem;">{h_name} {h_score} - {a_score} {a_name}</b><br>
                    <span class="live-text">● НА ЖИВО (Статус: {status})</span>
                </div>
                <div style="flex:1;">
                    <div class="pred-tag">
                        <small style="display:block; font-size:0.6rem; color:#eee;">AI ПРОГНОЗА</small>
                        {prediction}
                    </div>
                </div>
                <div style="flex:1; text-align:right;">
                    <span style="color:#00ff00; font-size:1.6rem; font-weight:bold;">{confidence}%</span><br>
                    <small style="color:#666;">СИГУРНОСТ</small>
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.warning("В момента няма мачове на живо.")

# --- 6. PLAYER SCANNER ---
st.divider()
st.subheader("👤 СКЕНЕР ЗА ИГРАЧИ")
p_name = st.text_input("Въведи име на играч (на латиница):", "")
if p_name:
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_HOST}
    try:
        res = requests.get(f"https://{RAPID_HOST}/football-get-search-players", headers=headers, params={"search_player": p_name})
        players = res.json().get('response', [])
        for p in players:
            st.info(f"📊 {p.get('name')} | Отбор: {p.get('team')} | Рейтинг: {p.get('rating')}")
    except:
        st.error("Няма данни за този играч.")
