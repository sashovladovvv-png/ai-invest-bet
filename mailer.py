import smtplib
from email.mime.text import MIMEText
import os

def send_daily_prognosis():
    # 1. Проверяваме дали имаме записани потребители
    if not os.path.exists("subscribers.txt"):
        print("Няма записани имейли.")
        return

    with open("subscribers.txt", "r") as f:
        emails = [line.strip() for line in f.readlines() if "@" in line]

    if not emails:
        print("Списъкът с имейли е празен.")
        return

    # 2. Генериране на съдържанието (Elite Double)
    # Тук можеш да вкараш логика, която взима мачовете от API-то
    subject = "🚨 Твоят Elite Double за днес е тук!"
    body = "Здравей!\n\nЕто днешните топ 2 прогнози от Equilibrium AI:\n1. Реал Мадрид - Барселона: Над 2.5 гола\n2. Ливърпул - Арсенал: Г/Г\n\nУспех!"

    # 3. Настройки на Gmail (Използвай App Password)
    sender = "your-email@gmail.com"
    password = "your-app-password"

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            for recipient in emails:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipient
                server.sendmail(sender, recipient, msg.as_string())
        print(f"✅ Успешно изпратено до {len(emails)} души.")
    except Exception as e:
        print(f"❌ Грешка при изпращане: {e}")

if __name__ == "__main__":
    send_daily_prognosis()