import streamlit as st
import os

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI", page_icon="📧", layout="centered")

# Дизайн
st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: white; }
    .main-title { color: #00ff00; text-align: center; font-family: 'Orbitron', sans-serif; font-size: 3rem; margin-top: 50px; text-shadow: 0 0 15px #00ff00; }
    .sub-text { text-align: center; color: #e0e0e0; font-size: 1.2rem; margin-bottom: 40px; }
    .email-container { background: #0d1117; padding: 40px; border-radius: 20px; border: 1px solid #1f242c; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    div.stButton > button { width: 100%; background-color: #00ff00; color: black; font-weight: bold; border: none; height: 50px; border-radius: 10px; }
    div.stButton > button:hover { background-color: #00cc00; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ГЛАВЕН ИНТЕРФЕЙС ---
st.markdown('<h1 class="main-title">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Остави имейла си и получавай ежедневните прогнози напълно безплатно</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="email-container">', unsafe_allow_html=True)
    
    email = st.text_input("Твоят имейл адрес:", placeholder="name@example.com")
    submit_btn = st.button("АБОНИРАЙ СЕ СЕГА")
    
    if submit_btn:
        if "@" in email and "." in email:
            # Записване във файл emails.txt
            with open("emails.txt", "a", encoding="utf-8") as f:
                f.write(f"{email}\n")
            
            st.success("✅ Успешно се записа за безплатните прогнози!")
            st.balloons()
        else:
            st.error("❌ Моля, въведи валиден имейл адрес.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. СКРИТ АДМИН ПАНЕЛ ЗА ТЕБ ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("Админ достъп"):
    password = st.text_input("Парола:", type="password")
    if password == "armada2026":
        st.subheader("📊 Списък с абонати:")
        if os.path.exists("emails.txt"):
            with open("emails.txt", "r", encoding="utf-8") as f:
                emails = f.readlines()
                if emails:
                    for i, e in enumerate(emails):
                        st.text(f"{i+1}. {e.strip()}")
                    st.download_button("ИЗТЕГЛИ СПИСЪКА", "".join(emails), file_name="subscribers.txt")
                else:
                    st.info("Няма нови абонати.")
        else:
            st.info("Списъкът е празен.")
