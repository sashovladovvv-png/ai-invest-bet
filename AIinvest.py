import streamlit as st
import pandas as pd
import soccerdata as sd
import math
import datetime
import pytz
import json
import os
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | GLOBAL ANALYZER", page_icon="🌍", layout="wide")
st_autorefresh(interval=600000, key="global_refresh")

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)

# --- 2. ИИ МОЗЪК (ПОАСОН АЛГОРИТЪМ) ---
def calculate_advanced_poisson(home_goals_avg, away_goals_avg):
    """Изчислява вероятност за Над 2.5 на база историческа резултатност"""
    lmbda = home_goals_avg + away_goals_avg
    # Формула за вероятност 0, 1 и 2 гола (Под 2.5)
    p0 = math.exp(-lmbda)
    p1 = math.exp(-lmbda) * lmbda
    p2 = (math.exp(-lmbda) * (lmbda**2)) / 2
    
    prob_under = (p0 + p1 + p2) * 100
    if prob_under < 50:
        return "НАД 2.5", round(100 - prob_under, 1)
    else:
        return "ПОД 2.5", round(prob_under, 1)

# --- 3. ФУНКЦИЯ ЗА СВЪРЗВАНЕ СЪС СВЕТОВНИТЕ ЛИГИ ---
@st.cache_data(ttl=3600)
def fetch_global_leagues_data():
    """Сваля информация за всички налични лиги през soccerdata"""
    all_leagues_data = {}
    try:
        # Използваме FiveThirtyEight за бърз достъп до глобални прогнози и статистики
        # Поддържа Англия, Германия, Испания, Италия, Франция, Холандия, САЩ, Бразилия и др.
        fte = sd.FiveThirtyEight(leagues="all", seasons=2025)
        upcoming = fte.read_upcoming()
        return upcoming
    except Exception as e:
        return None

# --- 4. СТИЛИЗАЦИЯ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 10px #00ff00; }
    .match-card { background: #0d1117; border: 1px solid #1f242c; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #00ff00; transition: 0.3s; }
    .match-card:hover { transform: scale(1.01); background: #161b22; }
    .league-label { background: #1f242c; color: #00ff00; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; }
    .prob-display { font-family: 'Orbitron'; color: #00ff00; font-size: 1.3rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. АДМИН ПАНЕЛ (ОБРАБОТКА НА ФАЙЛА) ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI | GLOBAL ENGINE</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.title("👤 АДМИН ПАНЕЛ")
    uploaded_file = st.file_uploader("Качи твоята АРМАДА (.txt)", type="txt")
    process_btn = st.button("🚀 АНАЛИЗИРАЙ СВЕТОВНИТЕ ЛИГИ")

# --- 6. ОСНОВНА ЛОГИКА И ПОДРЕЖДАНЕ ---
if uploaded_file or process_btn:
    with st.spinner("ИИ сканира световните лиги и анализира твоя файл..."):
        # 1. Извличане на глобалните данни
        global_stats = fetch_global_leagues_data()
        
        final_list = []
        
        # 2. Ако има качен файл, го анализираме
        if uploaded_file:
            content = uploaded_file.getvalue().decode("utf-8")
            for line in content.splitlines():
                if "," in line:
                    parts = line.split(",")
                    # Очакваме формат: Отбор1, Отбор2, Коефициент
                    h, a, odds = parts[0].strip(), parts[1].strip(), float(parts[2].strip())
                    pred, prob = calculate_advanced_poisson(1.6, 1.4) # Базово изчисление
                    final_list.append({
                        "league": "МОЯТ СПИСЪК", "match": f"{h} - {a}",
                        "pred": pred, "prob": prob, "time": "ДНЕС"
                    })

        # 3. Добавяме автоматично изтеглените мачове от света
        if global_stats is not None:
            for index, row in global_stats.head(20).iterrows():
                # Изчисляваме прогноза на база силата на отборите от soccerdata
                h_team = row['team1']
                a_team = row['team2']
                # Използваме готовите xG (очаквани голове) от библиотеката
                pred, prob = calculate_advanced_poisson(row['adj_score1'], row['adj_score2'])
                
                final_list.append({
                    "league": row.get('league', 'INTERNATIONAL'),
                    "match": f"{h_team} - {a_team}",
                    "pred": pred,
                    "prob": prob,
                    "time": row['date'].strftime("%H:%M")
                })

        # --- 4. АВТОМАТИЧНО ПОДРЕЖДАНЕ ---
        # Подреждаме всичко по процента на сигурност (prob)
        final_list = sorted(final_list, key=lambda x: x['prob'], reverse=True)

        # ПОКАЗВАНЕ НА РЕЗУЛТАТИТЕ
        st.subheader(f"✅ АНАЛИЗИРАНИ {len(final_list)} МАЧА (ПОДРЕДЕНИ ПО СИГУРНОСТ)")
        
        for m in final_list:
            st.markdown(f"""
                <div class="match-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="flex:2;">
                            <span class="league-label">{m['league']}</span><br>
                            <b style="font-size:1.1rem;">{m['match']}</b><br>
                            <small style="color:#666;">ЧАС: {m['time']}</small>
                        </div>
                        <div style="flex:1; text-align:center;">
                            <small style="color:#888;">AI ПРОГНОЗА</small><br>
                            <b style="color:#00ff00;">{m['pred']}</b>
                        </div>
                        <div style="flex:1; text-align:right;">
                            <span class="prob-display">{m['prob']}%</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # ПУБЛИЧНА ТАБЛИЦА С ИСТОРИЯ
        st.markdown("---")
        st.subheader("📊 ЦЯЛОСТНА ТАБЛИЦА НА АРМАДАТА")
        st.table(pd.DataFrame(final_list))

else:
    st.info("👈 Качи файл с мачове или натисни бутона, за да изтегля световната армада.")

st.markdown("<p style='text-align:center; color:#222; margin-top:50px;'>© 2026 EQUILIBRIUM AI | GLOBAL DATA PROCESSING</p>", unsafe_allow_html=True)
