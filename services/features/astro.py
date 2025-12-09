import requests
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

    res = requests.get(url)
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
    return data
