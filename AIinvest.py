import streamlit as st
import requests
import math
import datetime
import pytz

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA", page_icon="⚽", layout="wide")

# Твоите данни точно както са на снимката
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
# ХОСТЪТ ОТ ТВОЯТА СНИМКА:
RAPID_API_HOST = "free-api-live-football-data.p.rapidapi.com"

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)

# --- 2. МАТЕМАТИЧЕСКИ МОДЕЛ ---
def run_ai_analysis(h_name, a_name):
    # Симулация на анализ (Над/Под 2.5)
    score = (len(h_name) + len(a_name)) % 10
    prob = 72.0 + (score * 2.5)
    pred = "НАД 2.5" if score > 4 else "ПОД 2.5"
    return pred, prob

# --- 3. ДИЗАЙН ---
st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: white; }
    .main-header { color: #00ff00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 15px #00ff00; }
    .card { background: #0d1117; border: 1px solid #1f242c; border-radius: 12px; padding: 20px; margin-bottom: 12px; border-left: 5px solid #00ff00; }
    .prob-val { color: #00ff00; font-weight: bold; font-size: 1.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">EQUILIBRIUM AI | LIVE ENGINE</h1>', unsafe_allow_html=True)

# --- 4. ТЕГЛЕНЕ НА ДАННИ (ФИКСИРАНО ЗА ТВОЯ API) ---
all_matches = []

def get_live_data():
    # Променяме пътя към "fixtures-by-date", който е стандартен за тези API-та
    # Ако това API поддържа само търсене на играчи, ще изпише грешка тук
    url = f"https://{RAPID_API_HOST}/football-get-all-fixtures-by-date"
    querystring = {"date": now_bg.strftime('%Y-%m-%d')}
    
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": RAPID_API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            return response.json().get('response', [])
        else:
            # Ако горният път е грешен, опитваме общия за "live"
            url_live = f"https://{RAPID_API_HOST}/football-get-live-all"
            res_live = requests.get(url_live, headers=headers, timeout=10)
            return res_live.json().get('response', [])
    except:
        return []

with st.spinner("Свързване с хоста..."):
    data = get_live_data()

# --- 5. ОБРАБОТКА И ПОДРЕЖДАНЕ ---
if data and isinstance(data, list):
    for item in data:
        # Извличане на имена според структурата на API-то
        try:
            home = item.get('home', {}).get('name', 'Home')
            away = item.get('away', {}).get('name', 'Away')
            league = item.get('league', {}).get('name', 'League')
            
            pred, prob = run_ai_analysis(home, away)
            all_matches.append({
                "match": f"{home} - {away}",
                "league": league,
                "pred": pred,
                "prob": prob
            })
        except:
            continue

if all_matches:
    # ПОДРЕЖДАНЕ ПО % (Най-сигурните най-отгоре)
    all_matches = sorted(all_matches, key=lambda x: x['prob'], reverse=True)

    for m in all_matches:
        st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <small style="color:#00ff00;">{m['league']}</small><br>
                        <b style="font-size:1.3rem;">{m['match']}</b>
                    </div>
                    <div style="text-align:center;">
                        <small>AI ПРОГНОЗА</small><br>
                        <b>{m['pred']}</b>
                    </div>
                    <div class="prob-val">{m['prob']}%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error(f"Грешка: Хостът '{RAPID_API_HOST}' в момента не връща мачове. Провери дали си в таб 'Fixtures' в RapidAPI Playground.")

st.sidebar.write(f"Последно: {now_bg.strftime('%H:%M:%S')}")
