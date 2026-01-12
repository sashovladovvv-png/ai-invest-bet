import requests
import pandas as pd
import time
import random
import os

# --- КОНФИГУРАЦИЯ ---
CSV_FILE = "live_matches.csv"

def get_api_key():
    # Взима ключа, който си заложил в Aiinvest.py
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            return f.read().strip()
    return None

def mask_stake(base_percentage):
    """ 🛡️ ЗАЩИТА ОТ БОТОВЕ: Прави залога да изглежда човешки (напр. 5.14%) """
    return round(base_percentage + random.uniform(-0.18, 0.18), 2)

def fetch_real_live_matches():
    api_key = get_api_key()
    if not api_key:
        print("❌ Липсва API Ключ!")
        return

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"live": "all"} # Взима всички мачове, които се играят СЕГА
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        fixtures = data.get('response', [])
        signals = []

        print(f"📡 Скениране на {len(fixtures)} мача на живо...")

        for item in fixtures:
            fixture = item['fixture']
            teams = item['teams']
            goals = item['goals']
            # Взимаме статистиката (Опасни атаки)
            # Забележка: Някои мачове в безплатния план на API-то може да нямат пълна статистика
            stats = item.get('statistics', [])
            
            # Намираме опасните атаки за домакина (Home Team)
            da_home = 0
            if stats:
                for s in stats[0]['statistics']:
                    if s['type'] == 'Dangerous Attacks':
                        da_home = int(s['value']) if s['value'] else 0

            minute = fixture['status']['elapsed']
            score = f"{goals['home']}:{goals['away']}"
            
            # --- EQUILIBRIUM АЛГОРИТЪМ ---
            # Търсим мач след 25-та минута, където домакинът натиска (DA > Minute)
            if minute > 25 and da_home > minute:
                pressure_index = da_home / minute
                
                # Ако имаме "Gap" (Натискът е голям, но резултатът е равен или губят)
                if pressure_index > 1.1 and goals['home'] <= goals['away']:
                    
                    signals.append({
                        "match_name": f"{teams['home']['name']} vs {teams['away']['name']} ({score})",
                        "prediction": "EQUILIBRIUM GAP: NEXT GOAL HOME",
                        "odds": round(random.uniform(1.80, 2.60), 2), # В реална версия се взима от API-то
                        "stake": mask_stake(5.5),
                        "status": f"Pressure Index: {round(pressure_index, 2)} | DA: {da_home}"
                    })

        # Записваме истинските мачове в CSV-то за сайта
        if signals:
            pd.DataFrame(signals).to_csv(CSV_FILE, index=False)
            print(f"✅ Намерени {len(signals)} реални аномалии.")
        else:
            # Ако в момента няма аномалии по твоя модел, пишем "Scanning"
            pd.DataFrame([{"match_name": "Scanning...", "prediction": "Market in Equilibrium", "odds": "-", "stake": 0}]).to_csv(CSV_FILE, index=False)

    except Exception as e:
        print(f"❌ Грешка при връзка с API: {e}")

if __name__ == "__main__":
    while True:
        fetch_real_live_matches()
        # Изчакваме 2 минути преди следващото скениране, за да пестим API лимита
        time.sleep(120)
