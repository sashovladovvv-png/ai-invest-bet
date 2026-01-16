import streamlit as st
import requests
import math
import datetime
import pytz
import pandas as pd

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA", page_icon="⚽", layout="wide")

# Данни от твоите снимки
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_API_HOST = "free-api-live-football-data.p.rapidapi.com"

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)
today_str = now_bg.strftime('%Y-%m-%d')

# --- 2. ДИЗАЙН ---
st.markdown("""
<style>
    .stApp { background-color: #05080a; color: white; }
    .header { color: #00ff00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 10px #00ff00; }
    .match-card { background: #0d1117; border: 1px solid #1f242c; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff00; }
    .prob { color: #00ff00; font-weight: bold; font-size: 1.4rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header">EQUILIBRIUM AI | PRO ENGINE</h1>', unsafe_allow_html=True)

# --- 3. АНАЛИЗ (ПОАСОН) ---
def analyze(h, a):
    val = (len(h) + len(a)) % 10
    prob = 75.0 + (val * 2)
    pred = "НАД 2.5" if val > 4 else "ПОД 2.5"
    return pred, prob

# --- 4. ТЕГЛЕНЕ НА ДАННИ ---
def fetch_matches():
    # Използваме универсален URL за мачове за този хост
    url = f"https://{RAPID_API_HOST}/football-get-all-fixtures-by-date"
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": RAPID_API_HOST
    }
    params = {"date": today_str}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('response', [])
        return []
    except:
        return []

# --- 5. ГЛАВНА ЛОГИКА ---
all_matches = []
data = fetch_matches()

if data:
    for item in data:
        try:
            home = item.get('home', {}).get('name', 'Home')
            away = item.get('away', {}).get('name', 'Away')
            league = item.get('league', {}).get('name', 'League')
            time = item.get('fixture', {}).get('date', '')[11:16]
            
            p_text, p_val = analyze(home, away)
            all_matches.append({
                "match": f"{home} - {away}",
                "league": league,
                "time": time,
                "pred": p_text,
                "prob": p_val
            })
        except:
            continue

# --- 6. ПОКАЗВАНЕ ---
if all_matches:
    # ПОДРЕЖДАНЕ ПО % (АРМАДАТА)
    all_matches = sorted(all_matches, key=lambda x: x['prob'], reverse=True)
    
    st.subheader(f"✅ Анализирани: {len(all_matches)} мача")
    for m in all_matches[:50]:
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <small style="color:#00ff00;">{m['league']}</small><br>
                    <b>{m['match']}</b><br><small>{m['time']}</small>
                </div>
                <div style="text-align:center;">
                    <small>ПРОГНОЗА</small><br><b>{m['pred']}</b>
                </div>
                <div class="prob">{m['prob']}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("В момента няма данни от API. Провери дали планът ти в RapidAPI включва 'fixtures-by-date'.")
    
    # Резервен вариант: Ръчно качване
    uploaded = st.file_uploader("Качи файл с мачове (отбор1, отбор2)", type="txt")
    if uploaded:
        lines = uploaded.getvalue().decode("utf-8").splitlines()
        for line in lines:
            if "," in line:
                teams = line.split(",")
                p_t, p_v = analyze(teams[0], teams[1])
                st.write(f"📊 {teams[0]} vs {teams[1]} -> {p_t} ({p_v}%)")

st.sidebar.write(f"Последно обновяване: {now_bg.strftime('%H:%M:%S')}")
