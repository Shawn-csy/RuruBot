import requests
from bs4 import BeautifulSoup
import re
from typing import List

def radar() -> List[str]:

    try:
        url = 'https://www.cwa.gov.tw/V8/C/W/OBS_Radar.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')
        radar_images = soup.select('div.zoomHolder img.img-responsive')
        
        if not radar_images:
            radar_images = soup.select('img[alt="雷達回波"]')
        if not radar_images:
            img_tags = soup.find_all('img')
            image_urls = [i.get('src') for i in img_tags if i.get('src') and (re.search(r'radar', i.get('src'), re.IGNORECASE) or 'CV1_' in i.get('src'))]
        else:
            image_urls = [img.get('src') for img in radar_images if img.get('src')]
        
        full_urls = ['https://www.cwa.gov.tw' + url if not url.startswith('http') else url 
                    for url in image_urls]
        
        return full_urls[:2] if full_urls else []
        
    except Exception as e:
        print(f"獲取雷達圖時發生錯誤: {e}")
        return []
    
