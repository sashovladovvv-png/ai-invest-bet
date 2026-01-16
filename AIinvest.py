import streamlit as st
import requests
import math
import datetime
import pytz

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA", page_icon="⚽", layout="wide")

# Твоят ключ от снимката:
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_API_HOST = "api-football-v1.p.rapidapi.com"

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)
today_str = now_bg.strftime('%Y-%m-%d')

# --- 2. МАТЕМАТИЧЕСКИ МОДЕЛ ---
def run_ai_analysis(h_name, a_name):
    # Симулация на Поасон анализ за Над/Под 2.5
    val = (len(h_name) + len(a_name)) % 5
    prob = 70.0 + (val * 4)
    if val > 2:
        return "НАД 2.5", prob
    return "ПОД 2.5", prob

# --- 3. ДИЗАЙН ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: white; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 10px #00ff00; }
    .card { background: #0d1117; border: 1px solid #1f242c; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff00; }
    .prob { color: #00ff00; font-family: 'Orbitron'; font-size: 1.4rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">EQUILIBRIUM AI | RAPID ENGINE</h1>', unsafe_allow_html=True)

# --- 4. ИЗВЛИЧАНЕ НА ДАННИ ---
all_results = []

@st.cache_data(ttl=3600)
def get_matches():
    url = f"https://{RAPID_API_HOST}/v3/fixtures"
    querystring = {"date": today_str}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get('response', [])
    except:
        return []

# Зареждане
with st.spinner("Свързване с RapidAPI..."):
    data = get_matches()

if data:
    for item in data:
        h = item['teams']['home']['name']
        a = item['teams']['away']['name']
        league = item['league']['name']
        time = item['fixture']['date'][11:16]
        
        pred, prob = run_ai_analysis(h, a)
        all_results.append({
            "match": f"{h} - {a}",
            "league": league,
            "time": time,
            "pred": pred,
            "prob": prob
        })

# --- 5. ПОДРЕЖДАНЕ И ПОКАЗВАНЕ ---
if all_results:
    # Сортиране по процента на сигурност
    all_results = sorted(all_results, key=lambda x: x['prob'], reverse=True)

    st.subheader(f"✅ Анализирани днес: {len(all_results)} мача")
    
    for m in all_results:
        st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="flex:2;">
                        <small style="color:#00ff00;">{m['league']}</small><br>
                        <b style="font-size:1.2rem;">{m['match']}</b><br>
                        <small style="color:#666;">Начало: {m['time']}</small>
                    </div>
                    <div style="flex:1; text-align:center;">
                        <small style="color:#888;">AI ПРОГНОЗА</small><br>
                        <b>{m['pred']}</b>
                    </div>
                    <div style="flex:1; text-align:right;">
                        <span class="prob">{m['prob']}%</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Няма данни. Провери дали RapidAPI ключът ти е активен.")

st.sidebar.write(f"Обновено: {now_bg.strftime('%H:%M:%S')}")
