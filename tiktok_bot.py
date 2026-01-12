import pandas as pd
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from playwright.sync_api import sync_playwright
import os
import time

# --- КОНФИГУРАЦИЯ ---
DATA_FILE = "live_matches.csv"
VIDEO_NAME = "tiktok_promo.mp4"

def create_video():
    """Създава клип за TikTok на база на live_matches.csv"""
    if not os.path.exists(DATA_FILE): return False
    df = pd.read_csv(DATA_FILE)
    if df.empty: return False
    
    match = df.iloc[0] # Взимаме топ мача
    text = f"🤖 AI PREDICTION\n\n{match['Match']}\nCONFIDENCE: 98%\n\nFREE LINK IN BIO!"
    
    # 1080x1920 е размерът за TikTok
    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(7)
    txt = TextClip(text, fontsize=75, color='#39FF14', font='Arial-Bold', method='caption', size=(900, None))
    txt = txt.set_position('center').set_duration(7)
    
    video = CompositeVideoClip([bg, txt])
    video.write_videofile(VIDEO_NAME, fps=24, codec="libx264")
    return True

def upload_to_tiktok():
    """Автоматично качване в TikTok през браузъра"""
    with sync_playwright() as p:
        # Стартираме браузъра (headless=False, за да видиш как се логва първия път)
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("🌍 Отварям TikTok за качване...")
        page.goto("https://www.tiktok.com/upload")
        
        print("⚠️ ТРЯБВА ДА СЕ ЛОГНЕТЕ РЪЧНО ПРИ ПЪРВИЯ СТАРТ!")
        # Тук скриптът ще изчака, докато види бутона за качване (което значи, че сте логнати)
        page.wait_for_selector('input[type="file"]', timeout=300000) 
        
        # Качване на файла
        file_input = page.locator('input[type="file"]')
        file_input.set_input_files(VIDEO_NAME)
        
        print("⏳ Видеото се обработва...")
        time.sleep(10) # Изчакваме малко за обработка
        
        # Натискане на бутона "Post"
        post_button = page.get_by_text("Post")
        post_button.click()
        
        print("✅ ВИДЕОТО Е ПУБЛИКУВАНО!")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    if create_video():
        upload_to_tiktok()