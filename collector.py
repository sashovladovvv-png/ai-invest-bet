import time
import pandas as pd
import requests
import os
import random
import datetime
import math

# --- CORE ALGORITHM: EQUILIBRIUM MODEL ---

def calculate_equilibrium_gap(da_index, score_diff, time_elapsed, current_odds):
    """
    Изчислява 'Пропастта в равновесието'.
    Ако резултатът не отговаря на натиска (Dangerous Attacks), имаме аномалия.
    """
    # Математическо очакване за гол базирано на Dangerous Attacks (DA)
    expected_pressure = da_index / max(1, time_elapsed)
    
    # Коефициент на справедливост (Fair Odds)
    if expected_pressure > 1.5:
        fair_odds = 1.40
    elif expected_pressure > 1.0:
        fair_odds = 1.80
    else:
        fair_odds = 2.50
        
    # Equilibrium Gap: Разликата между пазарната цена и нашата изчислена цена
    gap = current_odds - fair_odds
    return gap, expected_pressure

def mask_bet_amount(base_stake):
    """
    ЛОГИКА ЗА МАСКИРОВКА (Anti-Limit Logic):
    Вместо фиксиран залог, алгоритъмът генерира сума, която изглежда 'човешка',
    за да предпази акаунта от лимитиране.
    """
    variation = random.uniform(-0.5, 0.5)
    masked_stake = round(base_stake + variation, 2)
    return masked_stake

def run_equilibrium_engine():
    print(f"🧩 [EQUILIBRIUM MODEL] Стартиране на анализ: {datetime.datetime.now()}")
    
    # Тези данни в идеалния случай идват от твоя API ключ
    # Симулираме реални live ситуации за Equilibrium анализ
    live_fixtures = [
        {"match": "Real Madrid vs Valencia", "score": "0:1", "min": 68, "da": 115, "odds": 2.45},
        {"match": "Man City vs Fulham", "score": "1:1", "min": 75, "da": 140, "odds": 1.95},
        {"match": "Milan vs Torino", "score": "0:0", "min": 32, "da": 55, "odds": 1.70}
    ]
    
    equilibrium_signals = []
    
    for game in live_fixtures:
        gap, pressure = calculate_equilibrium_gap(game['da'], 0, game['min'], game['odds'])
        
        # Ако пропастта в равновесието е значителна (> 0.30), генерираме сигнал
        if gap > 0.30:
            base_stake = 5.0 # Базов процент
            if pressure > 1.8: base_stake = 8.5
            
            final_stake = mask_bet_amount(base_stake)
            
            equilibrium_signals.append({
                "match_name": f"{game['match']} ({game['score']})",
                "prediction": "EQUILIBRIUM GAP DETECTED",
                "odds": game['odds'],
                "stake": final_stake,
                "status": f"Pressure: {round(pressure, 2)} | Gap: {round(gap, 2)}"
            })

    # Записваме в CSV за Aiinvest.py
    if equilibrium_signals:
        df = pd.DataFrame(equilibrium_signals)
        df.to_csv("live_matches.csv", index=False)
        print(f"✅ Намерени {len(equilibrium_signals)} точки на разцентроване в пазара.")
    else:
        # Празен файл с хедъри, за да не гърми сайта
        pd.DataFrame(columns=["match_name", "prediction", "odds", "stake", "status"]).to_csv("live_matches.csv", index=False)

if __name__ == "__main__":
    while True:
        try:
            run_equilibrium_engine()
        except Exception as e:
            print(f"Грешка: {e}")
        time.sleep(300) # Анализ на всеки 5 минути
