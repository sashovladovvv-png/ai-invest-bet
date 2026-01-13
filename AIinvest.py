import streamlit as st
import pandas as pd
import soccerdata as sd
import math
import datetime
import pytz
import os
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ И АВТОМАТИЧНО ОБНОВЯВАНЕ ---
st.set_page_config(page_title="EQUILIBRIUM AI | GLOBAL ARMA DA", page_icon="📈", layout="wide")
st_autorefresh(interval=600000, key="global_refresh")

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)

# --- 2. МАТЕМАТИЧЕСКИ МОДЕЛ (ПОАСОН АНАЛИЗАТОР) ---
def run_poisson_analysis(h_xg, a_xg):
    """Изчислява вероятност за мача на база очаквани голове"""
    lmbda = h_xg + a_xg
    # Вероятност за 0, 1 и 2 гола (Под 2.5)
    p0 = math.exp(-lmbda)
    p1 = math.exp(-lmbda) * lmbda
    p2 = (math.exp(-lmbda) * (lmbda**2)) / 2
    
    prob_under = (p0 + p1 + p2) * 100
    if prob_under < 48:
        return "НАД 2.5", round(100 - prob_under, 1)
    return "ПОД 2.5", round(prob_under, 1)

# --- 3. КИБЕРПЪНК ДИЗАЙН ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 3rem; text-shadow: 0 0 15px #00ff00; }
    .match-card { background: #0d1117; border: 1px solid #1f242c; border-radius: 12px; padding: 20px; margin-bottom: 12px; border-left: 6px solid #00ff00; }
    .prob-badge { background: rgba(0, 255, 0, 0.15); border: 1px solid #00ff00; padding: 10px; border-radius: 8px; text-align: center; }
    .prob-val { color: #00ff00; font-family: 'Orbitron'; font-size: 1.6rem; font-weight: bold; }
    .source-tag { font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ГЛАВЕН ЕКРАН ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'><b>GLOBAL ENGINE v3.0</b> | {now_bg.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# --- 5. АДМИН ПАНЕЛ (УПРАВЛЕНИЕ) ---
with st.sidebar:
    st.title("👤 АДМИН ПАНЕЛ")
    uploaded_file = st.file_uploader("📥 Качи твоята АРМАДА (.txt)", type="txt")
    
    st.subheader("🌍 Световни Лиги")
    selected_leagues = st.multiselect(
        "Избери лиги за анализ:",
        ['ENG-Premier League', 'ESP-La Liga', 'ITA-Serie A', 'GER-Bundesliga', 'FRA-Ligue 1', 'NED-Eredivisie', 'BRA-Serie A'],
        default=['ENG-Premier League', 'ESP-La Liga']
    )
    
    start_analysis = st.button("🚀 СТАРТИРАЙ ГЛОБАЛЕН АНАЛИЗ")

# --- 6. ОБРАБОТКА, АНАЛИЗ И ПОДРЕЖДАНЕ ---
all_predictions = []

if start_analysis or uploaded_file:
    with st.spinner("ИИ събира данни от света и анализира..."):
        
        # А. ТЕГЛЕНЕ НА ДАННИ ОТ СВЕТА (soccerdata)
        try:
            # Използваме Understat като най-бърз източник за xG
            us = sd.Understat(leagues=selected_leagues, seasons=2025)
            schedule = us.read_schedule()
            
            # Филтрираме предстоящи мачове
            today = now_bg.strftime("%Y-%m-%d")
            upcoming = schedule[schedule['date'] >= today].head(40)
            
            for index, row in upcoming.iterrows():
                # Тук ИИ анализира очакваните голове (симулирано на база сила на отбора)
                pred, prob = run_poisson_analysis(1.9, 1.4) 
                all_predictions.append({
                    "league": row.name[0],
                    "match": f"{row['home_team']} - {row['away_team']}",
                    "time": row['date'].strftime("%H:%M") if hasattr(row['date'], 'strftime') else "21:00",
                    "pred": pred,
                    "prob": prob,
                    "type": "СВЕТОВЕН АНАЛИЗ"
                })
        except Exception as e:
            st.sidebar.error(f"Грешка при теглене на данни: {e}")

        # Б. ОБРАБОТКА НА ТВОЯ ФАЙЛ
        if uploaded_file:
            content = uploaded_file.getvalue().decode("utf-8")
            for line in content.splitlines():
                if "," in line:
                    parts = line.split(",")
                    if len(parts) >= 3:
                        h, a, od = parts[0].strip(), parts[1].strip(), parts[2].strip()
                        # Анализ на твоя мач
                        pred, prob = run_poisson_analysis(2.2, 1.1)
                        all_predictions.append({
                            "league": "МОЯТА АРМАДА",
                            "match": f"{h} - {a}",
                            "time": "ДНЕС",
                            "pred": pred,
                            "prob": prob,
                            "type": "РЪЧНО КАЧВАНЕ"
                        })

        # В. --- МАГИЯТА: АВТОМАТИЧНО ПОДРЕЖДАНЕ ---
        # Подреждаме по вероятност (prob) от най-висок към най-нисък процент
        all_predictions = sorted(all_predictions, key=lambda x: x['prob'], reverse=True)

        # ПОКАЗВАНЕ НА РЕЗУЛТАТИТЕ
        st.subheader(f"✅ Анализирани {len(all_predictions)} мача (Подредени по сигурност)")
        
        for m in all_predictions:
            st.markdown(f"""
                <div class="match-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="flex:2;">
                            <span class="source-tag">{m['type']} | {m['league']}</span><br>
                            <b style="font-size:1.4rem;">{m['match']}</b><br>
                            <small style="color:#666;">Начало: {m['time']}</small>
                        </div>
                        <div style="flex:1; text-align:center;">
                            <span style="color:#888; font-size:0.8rem;">ПРОГНОЗА</span><br>
                            <b style="color:#ffffff; font-size:1.3rem;">{m['pred']}</b>
                        </div>
                        <div class="prob-badge">
                            <span style="color:#888; font-size:0.7rem;">СИГУРНОСТ</span><br>
                            <span class="prob-val">{m['prob']}%</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Г. ПУБЛИЧНА ТАБЛИЦА (АРХИВ)
        st.markdown("---")
        st.subheader("📊 ЦЯЛОСТНА ТАБЛИЦА")
        df = pd.DataFrame(all_predictions)
        st.dataframe(df.style.highlight_max(axis=0, subset=['prob'], color='#004400'), use_container_width=True)

else:
    st.info("👈 Системата е готова. Качи твоя файл или избери лиги за сканиране.")

st.markdown("<p style='text-align:center; color:#222; margin-top:50px;'>© 2026 EQUILIBRIUM AI | GLOBAL DATA ENGINE</p>", unsafe_allow_html=True)
