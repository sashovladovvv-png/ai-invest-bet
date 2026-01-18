import streamlit as st
import os

# --- 1. КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="EQUILIBRIUM AI | JOIN THE ARMADA", page_icon="📧", layout="centered")

# Дизайн - Изчистен и професионален
st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: white; }
    .main-title { color: #00ff00; text-align: center; font-family: 'Orbitron', sans-serif; font-size: 2.5rem; margin-top: 50px; }
    .sub-text { text-align: center; color: #888; margin-bottom: 30px; }
    .email-box { background: #161b22; padding: 30px; border-radius: 15px; border: 1px solid #00ff00; box-shadow: 0 0 20px rgba(0,255,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ГЛАВЕН ЕКРАН ---
st.markdown('<h1 class="main-title">EQUILIBRIUM AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Стани част от Армадата. Получавай най-сигурните AI прогнози директно в пощата си.</p>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="email-box">', unsafe_allow_html=True)
    
    email = st.text_input("Въведи своя имейл адрес:", placeholder="example@mail.com")
    submit_btn = st.button("ЗАПИШИ МЕ В АРМАДАТА")
    
    if submit_btn:
        if "@" in email and "." in email:
            # ЗАПИСВАНЕ НА ИМЕЙЛА ВЪВ ФАЙЛ
            with open("emails.txt", "a") as f:
                f.write(f"{email}\n")
            
            st.success("✅ Твоят имейл е записан успешно! Очаквай първите анализи скоро.")
            st.balloons()
        else:
            st.error("❌ Моля, въведи валиден имейл адрес.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. АДМИН ПАНЕЛ (ВИДИМ САМО ЗА ТЕБ) ---
# Можеш да добавиш парола, за да не ги виждат другите
st.markdown("---")
admin_key = st.text_input("Админ достъп (парола):", type="password")

if admin_key == "armada2026": # Твоята парола
    st.subheader("📊 Списък със записани имейли:")
    if os.path.exists("emails.txt"):
        with open("emails.txt", "r") as f:
            emails = f.readlines()
            if emails:
                for idx, e in enumerate(emails):
                    st.write(f"{idx+1}. {e.strip()}")
                
                # Бутон за изтегляне
                st.download_button("ИЗТЕГЛИ СПИСЪКА", "".join(emails), file_name="subscribers.txt")
            else:
                st.info("Все още няма записани имейли.")
    else:
        st.info("Файлът с имейли още не е създаден.")

st.markdown('<p style="text-align:center; color:#444; margin-top:100px;">Powered by Equilibrium AI Engine</p>', unsafe_allow_html=True)
