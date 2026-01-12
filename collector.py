import time
import pandas as pd
import random
import os
import datetime

# База данни за симулация на реални мачове
TEAMS = [
    "Manchester City", "Real Madrid", "Bayern Munich", "Liverpool", "PSG", 
    "Arsenal", "Barcelona", "Inter Milan", "Napoli", "AC Milan", 
    "Dortmund", "Atletico Madrid", "Juventus", "Bayer Leverkusen", "Benfica"
]

MARKETS = [
    "Над 2.5 Гола", "Победа за Домакина", "Двата отбора да отбележат", 
    "Азиатски Хендикап -1.0", "Над 1.5 Гола Първо Полувреме", "Под 3.5 Гола"
]

def generate_ai_analysis():
    print(f"🔄 [{datetime.datetime.now().strftime('%H:%M:%S')}] AI сканира пазара...")
    
    results = []
    # Генерираме случаен брой мачове (между 4 и 10)
    num_of_matches = random.randint(4, 10)
    
    for _ in range(num_of_matches):
        t1, t2 = random.sample(TEAMS, 2)
        match_name = f"{t1} vs {t2}"
        prediction = random.choice(MARKETS)
        odds = round(random.uniform(1.45, 3.50), 2)
        
        # Логика за залог: по-висок коефициент = по-нисък залог
        if odds < 1.80:
            stake = random.randint(6, 10)
        elif odds < 2.50:
            stake = random.randint(3, 6)
        else:
            stake = random.randint(1, 3)
            
        results.append({
            "match_name": match_name,
            "prediction": prediction,
            "odds": odds,
            "stake": stake
        })
    
    # Записваме в CSV
    df = pd.DataFrame(results)
    df.to_csv("live_matches.csv", index=False)
    print(f"✅ Успешно записани {len(results)} прогнози в live_matches.csv")

if __name__ == "__main__":
    print("🚀 AI COLLECTOR СТАРТИРАН...")
    while True:
        try:
            generate_ai_analysis()
        except Exception as e:
            print(f"❌ Критична грешка в колектора: {e}")
        
        # Обновява на всеки 5 минути (300 секунди)
        time.sleep(300)
