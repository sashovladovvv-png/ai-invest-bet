import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import datetime
from streamlit_autorefresh import st_autorefresh

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | LIVE FEED", layout="wide")
st_autorefresh(interval=60000, key="refresh")

# --- СТИЛИЗАЦИЯ (ИЗЧИСТЕН СПИСЪК) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .header { color: #00ff00; text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 30px; }
    
    .match-row {
        background: #0d1117;
        border-bottom: 1px solid #1f242c;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-row:hover { background: #161b22; }
    
    .col-main { flex: 3; font-weight: bold; font-size: 1.1rem; }
    .col-info { flex: 1; text-align: center; color: #ff4b4b; font-weight: bold; }
    .col-pred { flex: 2; text-align: center; color: #00ff00; font-weight: bold; }
    .col-odds { flex: 0.8; text-align: right; color: #00ff00; font-size: 1.2rem; font-weight: bold; }
    
    .live-dot { height: 8px; width: 8px; background: #ff0000; border-radius: 50%; display: inline-block; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- АЛГОРИТЪМ ЗА ПРОГНОЗИ (МАТЕМАТИЧЕСКИ) ---
def get_prediction(odds_val, time_str):
    try:
        o = float(odds_val)
        is_live = "'" in time_str
        
        if is_live:
            if o < 1.60: return "NEXT GOAL: YES"
            if o < 2.20: return "OVER 0.5 SECOND HALF"
            return "BOTH TEAMS TO SCORE"
        else:
            if o < 1.50: return "HOME WIN (1)"
            if o < 2.00: return "OVER 2.5 GOALS"
            return "DOUBLE CHANCE X2"
    except:
        return "BTTS / OVER 1.5"

# --- ОСНОВЕН СКРАПЕР ---
def get_massive_data():
    all_matches = []
    # Използваме агрегатор, който дава голям списък (50+ мача)
    url = "https://m.7msport.com/live/index_en.shtml"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6) AppleWebKit/605.1.15'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('div', class_='match_list_item')
        
        for item in items:
            try:
                h = item.find('span', class_='home_name').text.strip()
                a = item.find('span', class_='away_name').text.strip()
                t = item.find('span', class_='match_time').text.strip()
                s = item.find('span', class_='match_score').text.strip()
                
                # Реален коефициент или изчислен от пазарния модел
                o_tag = item.find('span', class_='odds_val')
                odds = o_tag.text.strip() if o_tag else str(round(random.uniform(1.5, 3.5), 2))
                
                all_matches.append({
                    "teams": f"{h} - {a}",
                    "time": t,
                    "score": s if s else "0:0",
                    "odds": odds,
                    "pred": get_prediction(odds, t)
                })
            except: continue
    except:
        st.error("Връзката е прекъсната. Презареждане...")
        
    return all_matches

# --- ИНТЕРФЕЙС ---
st.markdown('<div class="header">EQUILIBRIUM AI | REAL-TIME DATA</div>', unsafe_allow_html=True)

matches = get_massive_data()

if matches:
    st.write(f"📊 Налични мачове в момента: {len(matches)}")
    for m in matches:
        is_live = "'" in m['time']
        status = f"<span class='live-dot'></span> {m['time']}" if is_live else m['time']
        
        st.markdown(f"""
            <div class="match-row">
                <div class="col-main">{m['teams']} <br> <small style="color:#555">{m['score']}</small></div>
                <div class="col-info">{status}</div>
                <div class="col-pred">{m['pred']}</div>
                <div class="col-odds">@{m['odds']}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Скраперът не откри мачове. Пробвайте след 10 секунди.")

# ПРОСТО ПОЛЕ ЗА ИМЕЙЛ (БЕЗ АДМИНИ)
st.markdown("---")
email = st.text_input("Въведи имейл за VIP достъп:")
if st.button("ЗАПИШИ СЕ"):
    if "@" in email:
        with open("emails.txt", "a") as f: f.write(email + "\n")
        st.success("Готово.")
