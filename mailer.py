import time
import datetime
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- КОНФИГУРАЦИЯ (ПОПЪЛНИ ТУК) ---
GMAIL_USER = "твоят_мейл@gmail.com"
GMAIL_APP_PASS = "твоята_app_парола" # Трябва да е App Password от Google
CLIENT_LIST = ["client1@email.com", "client2@email.com"]

def send_bulk_emails():
    print("📧 Подготовка на имейлите...")
    
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = ", ".join(CLIENT_LIST)
    msg['Subject'] = f"🎯 AI INVESTOR: Вашите Прогнози за {datetime.date.today().strftime('%d.%m.%Y')}"

    # HTML Дизайн на имейла
    html = f"""
    <div style="background-color: #0b0e14; color: #ffffff; padding: 30px; border: 2px solid #00ff00; border-radius: 15px; font-family: sans-serif;">
        <h1 style="color: #00ff00; text-align: center;">AI INVESTOR SIGNALS</h1>
        <p style="font-size: 1.1em;">Здравейте, вашите анализи за днешния ден са готови!</p>
        <p>Нашият алгоритъм откри нови възможности с висока стойност.</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="ТВОЯТ_STREAMLIT_URL" style="background-color: #00ff00; color: #000; padding: 15px 25px; text-decoration: none; font-weight: bold; border-radius: 5px;">ВИЖ ПРОГНОЗИТЕ В САЙТА</a>
        </div>
        <p style="color: #555; font-size: 0.8em;">Ако не сте се абонирали за този бюлетин, моля игнорирайте съобщението.</p>
    </div>
    """
    
    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASS)
        server.sendmail(GMAIL_USER, CLIENT_LIST, msg.as_string())
        server.quit()
        print(f"✅ Успешно изпратени имейли до {len(CLIENT_LIST)} клиенти!")
    except Exception as e:
        print(f"❌ Грешка при изпращане на имейли: {e}")

def run_scheduler():
    # Проверка за ръчно стартиране
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        send_bulk_emails()
        return

    print("⏰ Мейлърът чака 10:00 часа (UTC 08:00)...")
    while True:
        now = datetime.datetime.now()
        
        # Настройка: 10:00 българско време е 08:00 UTC (Сървъра)
        if now.hour == 8 and now.minute == 0:
            send_bulk_emails()
            time.sleep(70) # Спираме за минута
            
        time.sleep(30) # Проверка на всеки 30 секунди

if __name__ == "__main__":
    run_scheduler()
