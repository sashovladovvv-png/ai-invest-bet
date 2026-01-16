import streamlit as st
import requests
import math
import datetime
import pytz
import pandas as pd

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | ARMA DA", page_icon="⚽", layout="wide")

# Твоят ключ от снимката
RAPID_API_KEY = "71f5127309mshc41229a206cf2a7p18854cjsn2cf570c49495"
RAPID_API_HOST = "api-football-v1.p.rapidapi.com"

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)
today_str = now_bg.strftime('%Y-%m-%d')

# --- 2. МАТЕМАТИКА ---
def simple_ai_logic(h, a):
    # Изчисляваме вероятност на база дължина на имената (докато заредим реални xG)
    score = (len(h) + len(a)) % 10
    prob = 65.0 + (score * 3)
    pred = "НАД 2.5" if score > 5 else "ПОД 2.5"
    return pred, prob

# --- 3. ДИЗАЙН ---
st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: white; }
    .main-header { color: #00ff00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 10px #00ff00; }
    .card { background: #0d1117; border: 1px solid #1f242c; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff00; }
    .error-box { background: #330000; color: #ff0000; padding: 10px; border-radius: 5px; border: 1px solid red; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">EQUILIBRIUM AI | GLOBAL ENGINE</h1>', unsafe_allow_html=True)

# --- 4. ТЕГЛЕНЕ НА ДАННИ С ДИАГНОСТИКА ---
all_matches = []

def fetch_data():
    url = f"https://{RAPID_API_HOST}/v3/fixtures"
    querystring = {"date": today_str}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # АКО ИМА ГРЕШКА В АБОНАМЕНТА, ТУК ЩЕ Я ВИДИМ
        if response.status_code != 200:
            return {"error": f"API Грешка {response.status_code}: {response.text}"}
        
        return response.json().get('response', [])
    except Exception as e:
        return {"error": f"Връзката прекъсна: {str(e)}"}

with st.spinner("Проверка на Армадата..."):
    result = fetch_data()

# Проверка дали резултатът е грешка или списък с мачове
if isinstance(result, dict) and "error" in result:
    st.markdown(f'<div class="error-box">⚠️ {result["error"]}</div>', unsafe_allow_html=True)
    st.info("💡 Провери дали си се абонирал за 'API-Football' (от API-SPORTS) в RapidAPI. Твоят ключ е активен, но трябва да имаш активен план за точно това API.")
elif not result:
    st.warning("Няма мачове за днешната дата в базата данни.")
else:
    # --- 5. ОБРАБОТКА И ПОДРЕЖДАНЕ ---
    for f in result:
        h = f['teams']['home']['name']
        a = f['teams']['away']['name']
        lg = f['league']['name']
        tm = f['fixture']['date'][11:16]
        
        prediction, probability = simple_ai_logic(h, a)
        all_matches.append({
            "match": f"{h} - {a}",
            "league": lg,
            "time": tm,
            "pred": prediction,
            "prob": probability
        })

    # СОРТИРАНЕ: Най-висок % първи
    all_matches = sorted(all_matches, key=lambda x: x['prob'], reverse=True)

    st.subheader(f"📊 Анализирани: {len(all_matches)} мача по света")
    
    for m in all_matches[:40]: # Показваме първите 40
        st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>{m['match']}</b><br><small>{m['league']} | {m['time']}</small></div>
                    <div style="text-align:center;"><b>{m['pred']}</b></div>
                    <div style="color:#00ff00; font-size:1.2rem; font-weight:bold;">{m['prob']}%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.sidebar.write(f"Последно обновяване: {now_bg.strftime('%H:%M:%S')}")
