import requests
import pandas as pd
import time
import random
import os

# --- КОНФИГУРАЦИЯ ---
API_FILE = "api_key.txt"
CSV_FILE = "live_matches.csv"

def get_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r") as f:
            return f.read().strip()
    return None

def mask_stake(base_percentage):
    """ 🛡️ ЗАЩИТА: Добавя шум към залога, за да изглежда като направен от човек """
    noise = random.uniform(-0.15, 0.15)
    return round(base_percentage + noise, 2)

def equilibrium_analysis():
    api_key = get_api_key()
    if not api_key:
        print("❌ Липсва API Ключ в api_key.txt")
        return

    print("🧠 Equilibrium Engine анализира пазара...")

    # В реална среда тук правиш requests.get към API-Football
    # За да видиш мачове ВЕДНАГА, генерираме живи сигнали по твоя модел:
    
    signals = []
    
    # ПРИМЕРНИ ДАННИ (Които алгоритъмът би извлякъл от API-то)
    potential_matches = [
        {"home": "Liverpool", "away": "Chelsea", "min": 65, "da": 88, "score": "0:0", "odds": 2.10},
        {"home": "Bayern", "away": "Dortmund", "min": 34, "da": 55, "score": "1:0", "odds": 1.65},
        {"home": "PSG", "away": "Monaco", "min": 78, "da": 110, "score": "1:1", "odds": 3.40}
    ]

    for match in potential_matches:
        # АЛГОРИТЪМ ЗА РАВНОВЕСИЕ:
        # Изчисляваме натиска спрямо времето (Dangerous Attacks / Minutes)
        pressure_index = match['da'] / match['min']
        
        # Ако натискът е висок (> 1.2), но резултатът е равен/губещ = Equilibrium Gap
        if pressure_index > 1.2:
            base_stake = 5.0 # Базов залог 5%
            if pressure_index > 1.5: base_stake = 8.5
            
            signals.append({
                "match_name": f"{match['home']} vs {match['away']} ({match['score']})",
                "prediction": "EQUILIBRIUM GAP DETECTED",
                "odds": match['odds'],
                "stake": mask_stake(base_stake), # ПРИЛАГА ЗАЩИТАТА
                "status": f"Pressure: {round(pressure_index, 2)} | Time: {match['min']}'"
            })

    # ЗАПИСВАНЕ - Критично важно за Aiinvest.py
    if signals:
        df = pd.DataFrame(signals)
        df.to_csv(CSV_FILE, index=False)
        print(f"✅ Успешно записани {len(signals)} сигнала.")
    else:
        # Ако няма мачове, създаваме празен файл с хедъри, за да не гърми сайта
        pd.DataFrame(columns=["match_name", "prediction", "odds", "stake", "status"]).to_csv(CSV_FILE, index=False)

if __name__ == "__main__":
    while True:
        try:
            equilibrium_analysis()
        except Exception as e:
            print(f"Грешка в колектора: {e}")
        
        # Скенира на всеки 5 минути (300 секунди)
        time.sleep(300)
