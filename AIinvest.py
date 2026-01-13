import streamlit as st
import json
import os
import datetime
import pytz
import math

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | AUTO-SORT", page_icon="🗂️", layout="wide")

bg_timezone = pytz.timezone('Europe/Sofia')
now_bg = datetime.datetime.now(bg_timezone)

DATA_FILE = "matches_db.json"
ADMIN_PASSWORD = "Nikol2121@"

# Инициализация на базата данни
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump([], f)

def load_data():
    try:
        with open(DATA_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except: return []

def save_data(data):
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- 2. АЛГОРИТЪМ ПОАСОН ---
def get_analysis(odds):
    try:
        o = float(odds)
        # Математически модел за очаквани голове
        lmbda = 3.25 / o
        p_under = (math.exp(-lmbda) * (1 + lmbda + (lmbda**2)/2)) * 100
        if p_under < 48:
            return "НАД 2.5", round(100 - p_under, 1)
        return "ПОД 2.5", round(p_under, 1)
    except: return "АНАЛИЗ", 50.0

# --- 3. ДИЗАЙН ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.8rem; text-shadow: 0 0 15px #00ff00; margin-bottom: 20px; }
    .match-card { background: #0d1117; border: 1px solid #1f242c; border-radius: 10px; padding: 20px; margin-bottom: 12px; border-left: 5px solid #00ff00; transition: 0.3s; }
    .match-card:hover { border-left: 5px solid #ffffff; background: #161b22; }
    .prob-badge { background: rgba(0, 255, 0, 0.1); color: #00ff00; padding: 5px 10px; border-radius: 5px; font-weight: bold; border: 1px solid #00ff00; }
    .table-style { width: 100%; border-collapse: collapse; margin-top: 30px; }
    .table-style th { background: #1f242c; color: #00ff00; padding: 12px; text-align: left; }
    .table-style td { padding: 12px; border-bottom: 1px solid #1f242c; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. АДМИН ПАНЕЛ (АВТОМАТИЗАЦИЯ) ---
with st.sidebar:
    st.title("⚙️ СИСТЕМЕН КОНТРОЛ")
    pwd = st.text_input("Парола за Nikol:", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.success("Системата е готова за зареждане")
        st.write("---")
        
        st.subheader("📦 МАСОВО ЗАРЕЖДАНЕ")
        # Позволява качване на целия файл с армадата мачове
        uploaded_file = st.file_uploader("Избери файл със статистика (.txt)", type="txt")
        
        if uploaded_file:
            content = uploaded_file.getvalue().decode("utf-8")
            lines = [line for line in content.splitlines() if line.strip()]
            
            new_data = []
            for line in lines:
                # Формат: Отбор1, Отбор2, Резултат, Коефициент, Час
                parts = line.split(",")
                if len(parts) >= 5:
                    h, a, sc, od, tm = [p.strip() for p in parts[:5]]
                    pred, prob = get_analysis(od)
                    new_data.append({
                        "match": f"{h} - {a}",
                        "score": sc,
                        "odds": od,
                        "pred": pred,
                        "prob": prob,
                        "time": tm,
                        "date": now_bg.strftime("%d.%m")
                    })
            
            # АВТОМАТИЧНО ПОДРЕЖДАНЕ: Сортираме по вероятност (най-сигурните най-отгоре)
            new_data = sorted(new_data, key=lambda x: x['prob'], reverse=True)
            
            if st.button("🚀 АНАЛИЗИРАЙ И ПОДРЕДИ"):
                save_data(new_data)
                st.balloons()
                st.rerun()

        if st.button("🗑️ ИЗЧИСТИ БАЗАТА"):
            save_data([])
            st.rerun()

# --- 5. ГЛАВЕН ЕКРАН (ВИЗУАЛИЗАЦИЯ) ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI | ENGINE</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#666;'>Последна синхронизация: {now_bg.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

data = load_data()

if not data:
    st.info("Системата очаква входни данни от Nikol. Използвайте админ панела за качване на армадата.")
else:
    st.subheader("🔥 ТОП ПРОГНОЗИ ЗА ДНЕС (ПОДРЕДЕНИ ПО СИГУРНОСТ)")
    for m in data:
        st.markdown(f"""
            <div class="match-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="flex:2;">
                        <b style="font-size:1.3rem; color:#fff;">{m['match']}</b><br>
                        <small style="color:#888;">ЧАС: {m['time']} | ДАТА: {m['date']}</small>
                    </div>
                    <div style="flex:1; text-align:center; color:#ff4b4b; font-family:Orbitron; font-size:1.6rem;">{m['score']}</div>
                    <div style="flex:1.5; text-align:center;">
                        <span class="prob-badge">{m['pred']} ({m['prob']}%)</span>
                    </div>
                    <div style="flex:0.5; text-align:right; color:#00ff00; font-weight:bold; font-size:1.2rem;">@{m['odds']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ПУБЛИЧНА ТАБЛИЦА С ИСТОРИЯ
    st.markdown("---")
    st.subheader("📈 ПУБЛИЧНА ИСТОРИЯ НА УСПЕВАЕМОСТТА")
    html_table = '<table class="table-style"><tr><th>ДАТА</th><th>МАЧ</th><th>ПРОГНОЗА</th><th>ВЕРОЯТНОСТ</th><th>СТАТУС</th></tr>'
    for m in data:
        html_table += f"<tr><td>{m['date']}</td><td>{m['match']}</td><td>{m['pred']}</td><td>{m['prob']}%</td><td style='color:#00ff00;'>АКТИВЕН ✅</td></tr>"
    html_table += '</table>'
    st.markdown(html_table, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#222; margin-top:50px;'>© 2026 EQUILIBRIUM AI | DATA ANALYTICS SYSTEM</p>", unsafe_allow_html=True)
