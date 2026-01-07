import requests
import time
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from services.constants import astro, astro_type




def get_astro_info(astro_name: str, type: str):
    # 使用台灣時區獲取今天的日期
    taipei_tz = pytz.timezone('Asia/Taipei')
    today = datetime.now(taipei_tz).strftime("%Y-%m-%d")
    index = astro[astro_name]
    if type == "weekly":    
        url = f'https://astro.click108.com.tw/weekly_1.php?iAcDay={today}&iType=1&iAstro={index}'
    elif type == "daily":
        url = f'https://astro.click108.com.tw/daily_0.php?iAstro={index}&iAcDay={today}'

    max_retries = 3
    for attempt in range(max_retries):
        try:
            res = requests.get(url, timeout=15)
            if res.status_code != 200:
                print(f"Attempt {attempt + 1}: HTTP {res.status_code}")
                continue

            soup = BeautifulSoup(res.text, 'html.parser')
            today_word_elements = soup.find_all('div', class_='TODAY_WORD', )
            todayFeature = soup.find_all('div', class_='TODAY_CONTENT')
            data = []
            for i in todayFeature:
                data.append(i.text)
            for i in today_word_elements:
                p_tags = i.find_all('p')
                for j in p_tags:
                    data.append(j.text)
            
            if data:
                return data
            
            print(f"Attempt {attempt + 1}: Empty data received")
            
        except requests.Timeout:
            print(f"Attempt {attempt + 1}: Timeout")
        except Exception as e:
            print(f"Attempt {attempt + 1}: {e}")
            
        if attempt < max_retries - 1:
            time.sleep(2)
            
    return ["無法獲取星座運勢，請稍後再試"]
