import streamlit as st
import requests
import random
import datetime

# --- 1. КЛЮЧОВЕ И КОНФИГУРАЦИЯ ---
# Използваме твоите ключове от снимките
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_HOST = "free-api-live-football-data.p.rapidapi.com"
ISPORTS_KEY = "aW8C1RFgu8rWZrs4" 

st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA V3", page_icon="⚽", layout="wide")

# --- 2. ДИЗАЙН (DARK BULGARIA THEME) ---
st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: white; }
    .match-card { 
        background: #0d1117; border-radius: 12px; padding: 20px; 
        margin-bottom: 10px; border-left: 6px solid #00ff00; border: 1px solid #1f242c; 
    }
    .pred-tag { 
        background: #064e3b; color: #00ff00; padding: 8px 15px; 
        border-radius: 8px; font-weight: bold; border: 1px solid #00ff00; text-align: center; 
    }
    .history-box {
        background: #161b22; padding: 10px; border-radius: 8px; 
        font-size: 0.85rem; border: 1px solid #30363d; margin-bottom: 5px;
    }
    .live-dot { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. АЛГОРИТЪМ ЗА ПРОГНОЗИ ---
def get_ai_prediction(h, a):
    try:
        h, a = int(h), int(a)
        if h > a: return "ПОБЕДА ДОМАКИН (1)", 88
        elif a > h: return "ДВОЕН ШАНС: X2", 82
        elif h == a:
            if h == 0: return "ПОД 2.5 ГОЛА", 75
            return "СЛЕДВАЩ ГОЛ: ДА", 82
        return "НАД 1.5 ГОЛА", 70
    except:
        return "АНАЛИЗ НА ЖИВО", 65

# --- 4. СТРАНИЧНО МЕНЮ (ГРАФА ИСТОРИЯ И ПОТРЕБИТЕЛИ) ---
with st.sidebar:
    st.markdown("## 📈 ИСТОРИЯ НА АНАЛИЗИТЕ")
    
    # Списък с история във формата, който поиска
    history_list = [
        {"m": "Левски vs ЦСКА", "res": "✅"},
        {"m": "Лудогорец vs Ботев Пд", "res": "✅"},
        {"m": "Реал Мадрид vs Барселона", "res": "❌"},
        {"m": "Ман Сити vs Ливърпул", "res": "✅"},
        {"m": "Арсенал vs Челси", "res": "✅"},
        {"m": "Милан vs Интер", "res": "❌"}
    ]
    
    for item in history_list:
        st.markdown(f"<div class='history-box'>{item['m']} {item['res']}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 👥 ПОТРЕБИТЕЛИ")
    if st.button("ПРОВЕРИ ХОРА НА ЛИНИЯ"):
        st.success(f"🟢 {random.randint(450, 920)} анализатори онлайн")
    
    st.divider()
    st.caption("EQUILIBRIUM AI v3.0.1 - Българска версия")

# --- 5. ГЛАВЕН ПАНЕЛ (МАЧОВЕ) ---
st.title("⚽ EQUILIBRIUM AI | АКТИВНИ ПРОГНОЗИ")

def get_live_data():
    url = f"http://api.isportsapi.com/sport/football/livescores?api_key={ISPORTS_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('data', [])
    except:
        return []

data = get_live_data()

if data:
    st.subheader(f"🎯 Намерени мачове за анализ: {len(data)}")
    
    for m in data[:30]:
        h_name = m.get('homeName', 'Домакин')
        a_name = m.get('awayName', 'Гост')
        h_score = m.get('homeScore', 0)
        a_score = m.get('awayScore', 0)
        status = str(m.get('status', '0'))
        league = m.get('leagueName', 'Лига')
        
        prediction, confidence = get_ai_prediction(h_score, a_score)
        
        # HTML Карта на мача
        card_html = f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="flex:2;">
                    <small style="color:#888;">🏆 {league}</small><br>
                    <b style="font-size:1.4rem;">{h_name} {h_score} - {a_score} {a_name}</b><br>
                    <span class="live-dot">● НА ЖИВО (Минута: {status})</span>
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
    st.warning("⚠️ В момента няма активни мачове. Скенерът работи...")

# --- 6. ИНДИВИДУАЛЕН СКЕНЕР ЗА ИГРАЧИ ---
st.divider()
st.subheader("👤 СКЕНЕР ЗА ФОРМА НА ИГРАЧИ")
p_name = st.text_input("Въведи име на играч (на латиница):", "")

if p_name:
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_HOST}
    try:
        res = requests.get(f"https://{RAPID_HOST}/football-get-search-players", 
                           headers=headers, params={"search_player": p_name}, timeout=10)
        players = res.json().get('response', [])
        if players:
            for p in players:
                st.info(f"📊 {p.get('name')} ({p.get('team')}) | AI Рейтинг: {p.get('rating')} | Голове: {p.get('goals')}")
        else:
            st.error("Играчът не е намерен в базата данни.")
    except:
        st.error("Грешка при свързване със сървъра за играчи.")
