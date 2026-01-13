import streamlit as st
import requests
import random
import math
import datetime
import pytz
import json
import os
from bs4 import BeautifulSoup
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ И ЧАСОВА ЗОНА ---
st.set_page_config(page_title="EQUILIBRIUM AI | LIVE ARCHIVE", page_icon="📈", layout="wide")
st_autorefresh(interval=60000, key="bot_refresh")

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)

ARCHIVE_FILE = "match_history.json"
ADMIN_PASSWORD = "Nikol2121@"

# Инициализация на архива, ако не съществува
if not os.path.exists(ARCHIVE_FILE):
    with open(ARCHIVE_FILE, "w") as f:
        json.dump([], f)

# --- 2. СТИЛИЗАЦИЯ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.8rem; text-shadow: 0 0 15px #00ff00; }
    
    .match-row { background: rgba(13, 17, 23, 0.98); border: 1px solid #1f242c; border-radius: 8px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .match-row-live { border-left: 5px solid #ff4b4b; }
    
    .archive-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #0d1117; border-radius: 10px; overflow: hidden; }
    .archive-table th { background: #1f242c; color: #00ff00; padding: 12px; text-align: left; }
    .archive-table td { padding: 12px; border-bottom: 1px solid #1f242c; }
    .status-win { color: #00ff00; font-weight: bold; }
    .status-loss { color: #ff4b4b; font-weight: bold; }
    
    .score-display { color: #ff4b4b; font-family: 'Orbitron'; font-size: 1.4rem; font-weight: bold; margin: 0 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ФУНКЦИИ ЗА АРХИВА ---
def save_to_archive(match_data):
    with open(ARCHIVE_FILE, "r") as f:
        history = json.load(f)
    # Избягване на дубликати
    if not any(h['match'] == match_data['match'] for h in history[-20:]):
        history.append(match_data)
        with open(ARCHIVE_FILE, "w") as f:
            json.dump(history[-100:], f) # Пазим последните 100 мача

def get_archive():
    with open(ARCHIVE_FILE, "r") as f:
        return json.load(f)

# --- 4. АЛГОРИТЪМ ПОАСОН ---
def calculate_poisson(odds):
    try:
        o = float(odds)
        lmbda = 3.25 / o
        p_under = (math.exp(-lmbda) * (1 + lmbda + (lmbda**2)/2)) * 100
        if p_under < 48: return "НАД 2.5", f"{100-p_under:.1f}%"
        return "ПОД 2.5", f"{p_under:.1f}%"
    except: return "АНАЛИЗ", "---"

# --- 5. DATA ENGINE ---
def get_matches():
    results = []
    url = "https://www.scorespro.com/rss2/soccer.xml"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        for item in soup.find_all('item'):
            title = item.title.text
            if " vs " in title or " - " in title:
                score = "0 - 0"
                for w in title.split():
                    if "-" in w and any(c.isdigit() for c in w): score = w; break
                
                clean_title = title.replace(score, "").strip()
                o = str(round(random.uniform(1.5, 3.8), 2))
                pred, prob = calculate_poisson(o)
                is_live = any(char.isdigit() for char in score) and score != "0-0"
                
                results.append({
                    "match": clean_title, "score": score, "odds": o,
                    "pred": pred, "prob": prob, "is_live": is_live
                })
                
                # Симулация на автоматично архивиране за приключили мачове (примерно)
                if "FT" in title or "Finished" in title:
                    goals = sum(int(x) for x in score.split('-') if x.isdigit())
                    status = "ПЕЧЕЛИ ✅" if (pred == "НАД 2.5" and goals > 2.5) or (pred == "ПОД 2.5" and goals < 2.5) else "ГУБИ ❌"
                    save_to_archive({"date": now_bg.strftime("%d.%m"), "match": clean_title, "res": score, "pred": pred, "status": status})
                    
    except: pass
    return sorted(results, key=lambda x: x['is_live'], reverse=True)

# --- 6. ГЛАВЕН UI ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'>Българско време: {now_bg.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# Секция: Мачове на живо и предстоящи
st.subheader("🎯 АКТУАЛНИ ПРОГНОЗИ")
matches = get_matches()
for m in matches[:30]:
    l_class = "match-row-live" if m['is_live'] else ""
    st.markdown(f"""
        <div class="match-row {l_class}">
            <div style="flex:3;"><b>{m['match']}</b><br><small>{'🔴 НА ЖИВО' if m['is_live'] else 'ПРЕДСТОЯЩ'}</small></div>
            <div class="score-display">{m['score']}</div>
            <div style="flex:2; text-align:center; background:rgba(0,255,0,0.05); border-radius:5px; padding:5px;">
                <span style="color:#00ff00;">{m['pred']}</span><br><small>{m['prob']}</small>
            </div>
            <div style="flex:0.8; text-align:right; font-weight:bold;">@{m['odds']}</div>
        </div>
    """, unsafe_allow_html=True)

# Секция: ПУБЛИЧЕН АРХИВ (Таблица на екрана)
st.markdown("---")
st.subheader("📊 ИСТОРИЯ И УСПЕВАЕМОСТ (Архив)")
history_data = get_archive()

if history_data:
    html_table = '<table class="archive-table"><tr><th>Дата</th><th>Мач</th><th>Резултат</th><th>Прогноза</th><th>Статус</th></tr>'
    for h in reversed(history_data[-15:]): # Показваме последните 15 записи
        status_class = "status-win" if "✅" in h['status'] else "status-loss"
        html_table += f"<tr><td>{h['date']}</td><td>{h['match']}</td><td>{h['res']}</td><td>{h['pred']}</td><td class='{status_class}'>{h['status']}</td></tr>"
    html_table += '</table>'
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.info("Архивът се обновява... Очаквайте първите резултати след приключване на мачовете.")

# --- 7. АДМИН МЕНЮ ---
with st.sidebar:
    st.title("🔐 АДМИН")
    pwd = st.text_input("Парола:", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Достъп за Nikol разрешен")
        if st.button("ИЗТРИЙ АРХИВА"):
            with open(ARCHIVE_FILE, "w") as f: json.dump([], f)
            st.rerun()

st.markdown("<p style='text-align:center; color:#222; margin-top:50px;'>© 2026 EQUILIBRIUM AI | ПУБЛИЧНА ИСТОРИЯ</p>", unsafe_allow_html=True)
