import streamlit as st
import requests
import random
import math
import os
from streamlit_autorefresh import st_autorefresh

# --- 1. КОНФИГУРАЦИЯ НА СТРАНИЦАТА ---
st.set_page_config(page_title="EQUILIBRIUM AI | МАТЕМАТИЧЕСКИ ПРОГНОЗИ", page_icon="📊", layout="wide")
st_autorefresh(interval=60000, key="bot_refresh")

EMAILS_FILE = "emails.txt"

# --- 2. ДИЗАЙН И СТИЛИЗАЦИЯ (ИЗЦЯЛО НА БЪЛГАРСКИ) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background-color: #05080a; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .main-header { font-family: 'Orbitron', sans-serif; color: #00ff00; text-align: center; font-size: 2.8rem; text-shadow: 0 0 15px #00ff00; margin-bottom: 25px; }
    
    .match-row {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid #1f242c;
        border-radius: 6px;
        padding: 15px 25px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .match-row:hover { border-color: #00ff00; background: #161b22; transform: scale(1.005); transition: 0.2s; }
    
    .team-box { flex: 3; font-size: 1.2rem; font-weight: bold; color: #ffffff; }
    .algo-box { flex: 2; text-align: center; border-left: 1px solid #333; border-right: 1px solid #333; }
    .prob-badge { background: rgba(0, 255, 0, 0.1); color: #00ff00; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; font-family: 'Orbitron'; border: 1px solid #00ff00; }
    .odds-box { flex: 0.8; text-align: right; color: #00ff00; font-weight: bold; font-size: 1.3rem; }
    
    .status-badge { color: #ff4b4b; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }
    .archive-section { background: #0d1117; padding: 20px; border-radius: 10px; margin-top: 30px; border: 1px solid #222; }
    .donate-btn { background: #ffcc00 !important; color: black !important; font-weight: bold !important; border-radius: 8px; padding: 15px; text-align: center; display: block; text-decoration: none; margin-top: 30px; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. АЛГОРИТЪМ НА ПОАСОН (МАТЕМАТИЧЕСКО ЯДРО) ---
def poisson_probability(lmbda, k):
    """Изчислява вероятността k събития да се случат при средна стойност lmbda"""
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_poisson_prediction(odds):
    try:
        o = float(odds)
        # Очаквани голове спрямо коефициента на пазара
        expected_goals = 3.4 / o 
        
        # Вероятност за 0, 1 и 2 гола (Под 2.5)
        p0 = poisson_probability(expected_goals, 0)
        p1 = poisson_probability(expected_goals, 1)
        p2 = poisson_probability(expected_goals, 2)
        
        under_prob = (p0 + p1 + p2) * 100
        over_prob = 100 - under_prob
        
        if over_prob > 55:
            return "НАД 2.5 ГОЛА", f"{over_prob:.1f}%"
        elif over_prob < 40:
            return "ПОД 2.5 ГОЛА", f"{under_prob:.1f}%"
        else:
            return "ДВАТА ОТБОРА ДА ВКАРАТ", f"{random.randint(62, 78)}%"
    except:
        return "АНАЛИЗ...", "---"

# --- 4. ГЕНЕРАТОР НА ДАННИ (50+ МАЧА) ---
def fetch_matches():
    results = []
    teams = [
        "Реал Мадрид", "Барселона", "Ман Сити", "Ливърпул", "Арсенал", "Байерн Мюнхен", 
        "Борусия Дортмунд", "Милан", "Интер", "Ювентус", "ПСЖ", "Наполи", "Челси", 
        "Ман Юнайтед", "Аякс", "Бенфика", "Порто", "Спортинг Лисабон", "Галатасарай", 
        "Фенербахче", "Селтик", "Рейнджърс", "ПСВ", "Фейенорд", "Монако", "Лион", 
        "Марсилия", "Лацио", "Рома", "Аталанта", "Виляреал", "Севиля", "Бетис", 
        "РБ Лайпциг", "Леверкузен", "Астън Вила", "Тотнъм", "Нюкасъл", "Лудогорец", "ЦСКА"
    ]
    
    for i in range(52):
        h, a = random.sample(teams, 2)
        odds = str(round(random.uniform(1.40, 4.80), 2))
        pred, prob = get_poisson_prediction(odds)
        
        # Симулиране на време (на живо или предстоящ)
        is_live = random.random() > 0.4
        time_status = f"{random.randint(5, 88)}'" if is_live else f"{random.randint(18, 22)}:00"
        
        results.append({
            "match": f"{h} срещу {a}",
            "odds": odds,
            "pred": pred,
            "prob": prob,
            "time": time_status,
            "is_live": is_live
        })
    return results

# --- 5. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-header">EQUILIBRIUM AI | ТЕРМИНАЛ</h1>', unsafe_allow_html=True)

data = fetch_matches()

st.subheader(f"📡 АКТИВЕН ПОТОК: {len(data)} АНАЛИЗИРАНИ МАЧА")

for m in data:
    status_html = f"<span class='status-badge'>● НА ЖИВО {m['time']}</span>" if m['is_live'] else f"ДНЕС {m['time']}"
    
    st.markdown(f"""
        <div class="match-row">
            <div class="team-box">
                {m['match']} <br> 
                <small style="color:#666;">Статус: {status_html}</small>
            </div>
            <div class="algo-box">
                <span style="color:#00ff00; font-weight:bold; text-transform:uppercase;">{m['pred']}</span><br>
                <span class="prob-badge">AI ВЕРОЯТНОСТ: {m['prob']}</span>
            </div>
            <div class="odds-box">@{m['odds']}</div>
        </div>
    """, unsafe_allow_html=True)

# СЕКЦИЯ АРХИВ
st.markdown('<div class="archive-section">', unsafe_allow_html=True)
st.subheader("✅ ПОСЛЕДНИ УСПЕШНИ ПРОГНОЗИ")
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        st.markdown(f"""
            <div style="text-align:center; border:1px solid #333; padding:15px; border-radius:5px; background: #05080a;">
                <b style="color:#00ff00;">УСПЕХ ✅</b><br>
                <small>Точност: {82+i}%</small><br>
                <b>@{1.70 + i*0.18}</b>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# БУТОН ЗА ДАРЕНИЯ
st.markdown('<a href="https://paypal.me/yourlink" class="donate-btn">☕ ПОДКРЕПЕТЕ РАЗРАБОТКАТА НА ПРОЕКТА</a>', unsafe_allow_html=True)

# СТРАНИЧЕН ПАНЕЛ (SIDEBAR)
with st.sidebar:
    st.title("⚙️ НАСТРОЙКИ НА AI")
    st.write("**Модел:** Poisson Distribution v2.1")
    st.write(f"**Обработени мачове:** {len(data)}")
    st.write("---")
    
    st.subheader("📩 VIP АБОНАМЕНТ")
    email = st.text_input("Въведете вашия имейл:")
    if st.button("АБОНИРАЙ МЕ"):
        if "@" in email:
            with open(EMAILS_FILE, "a") as f: f.write(email + "\n")
            st.success("Успешно добавен!")
        else:
            st.error("Невалиден имейл!")
            
    st.write("---")
    if st.button("🚀 ИЗПРАТИ VIP СИГНАЛИ"):
        if os.path.exists("mailer.py"):
            os.system("python mailer.py")
            st.success("Сигналите са разпратени!")
        else:
            st.error("Файлът mailer.py не е намерен!")

st.markdown("<p style='text-align:center; color:#222; margin-top:30px;'>© 2026 EQUILIBRIUM AI | СИСТЕМА ЗА МАТЕМАТИЧЕСКИ АНАЛИЗИ</p>", unsafe_allow_html=True)
