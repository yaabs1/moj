import requests
from bs4 import BeautifulSoup

# --- تنظیمات ---
# لینکی که از مرحله قبل (Deploy) گرفتید را اینجا بگذارید
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzvCTed8LXlUt_Em0uYf8fWGNiJ99znOH04J5xzev9Ori27Nya6l1Spf1x7mIgq3Doc/exec"
ALALAM_NEWS_URL = "https://www.alalam.com/ar/news"

def scrape_and_send():
    print("🔍 در حال بررسی سایت العالم...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # 1. دریافت محتوای سایت
        response = requests.get(ALALAM_NEWS_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. پیدا کردن آخرین خبر (این بخش باید با کلاس سایت العالم ست شود)
        # فرض می‌کنیم خبر در تگ h2 است
        news_element = soup.find('h2') 
        
        if news_element:
            news_text = news_element.get_text(strip=True)
            print(f"✅ خبر پیدا شد: {news_text[:50]}...")
            
            # 3. ارسال به گوگل (بدون نیاز به Service Account و فیلترشکن)
            payload = {
                'action': 'receiveNewsFromBot',
                'text': news_text
            }
            
            # استفاده از GET برای ارسال ساده به Apps Script
            resp = requests.get(GOOGLE_SCRIPT_URL, params=payload)
            
            if resp.status_code == 200:
                print("🚀 خبر با موفقیت به گوگل شیت ارسال شد!")
            else:
                print(f"❌ خطا در ارسال به گوگل: {resp.status_code}")
        else:
            print("⚠️ خبری پیدا نشد.")
            
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    scrape_and_send()
