import requests
import pandas as pd
import time
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
API_KEY = "b4c92379d14d40edb87a9f3412d6835f"
URL = "https://api.football-data.org/v4/matches"
HEADERS = {'X-Auth-Token': API_KEY}
DATA_FILE = "live_matches.csv"
REFRESH_INTERVAL = 15 * 60  # 15 минути

# Списък с Топ 10 първенства (Кодовете им в API-то)
TOP_LEAGUES_IDS = [2021, 2001, 2002, 2019, 2014, 2015, 2013, 2003, 2017, 2146]

def fetch_live_data():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Свързване с базата данни за LIVE мачове...")
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            matches_list = []
            for m in matches:
                # Филтрираме само мачове, които се играят в момента или предстоят днес
                league_id = m['competition']['id']
                if league_id in TOP_LEAGUES_IDS:
                    h_team = m['homeTeam']['name']
                    a_team = m['awayTeam']['name']
                    h_score = m['score']['fullTime']['home'] if m['score']['fullTime']['home'] is not None else 0
                    a_score = m['score']['fullTime']['away'] if m['score']['fullTime']['away'] is not None else 0
                    
                    matches_list.append({
                        "Match": f"{h_team} - {a_team}",
                        "Score": f"{h_score}:{a_score}",
                        "League": m['competition']['name'],
                        "Updated": datetime.now().strftime("%H:%M")
                    })
            
            if matches_list:
                df = pd.DataFrame(matches_list)
                df.to_csv(DATA_FILE, index=False)
                print(f"✅ Успешно записани {len(df)} елитни мача.")
            else:
                print("⚠️ В момента няма активни мачове в топ 10 първенствата.")
                # Записваме празен файл с хедъри, за да не гърми Aiinvest
                pd.DataFrame(columns=["Match", "Score", "League", "Updated"]).to_csv(DATA_FILE, index=False)
        else:
            print(f"❌ API Грешка: {response.status_code}. Провери ключа си.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {e}")

if __name__ == "__main__":
    print("🚀 API COLLECTOR Е СТАРТИРАН (Фокус: Топ 10 лиги)")
    while True:
        fetch_live_data()
        time.sleep(REFRESH_INTERVAL)