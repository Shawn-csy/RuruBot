import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def get_podcast():
    url = "https://podcasts.apple.com/tw/podcast/%E5%94%90%E9%99%BD%E9%9B%9E%E9%85%92%E5%B1%8B/id1536374746"
    res = requests.get(url)


    if res.status_code != 200:
        return 

    def timedefine(podcasttime):
        try:
            date_time1 = datetime.today()
            date_time2 = datetime.strptime(podcasttime, "%Y-%m-%d")
            difference = date_time1 - date_time2
            return difference.days
        except ValueError as ve:
            return None

    html_content = res.content.decode()
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find("script", {"id": "schema:show"})


    if not script_tag:
        return None

    try:
        json_data = script_tag.string
        podcast_info = json.loads(json_data)
        workdata = podcast_info['workExample']
        
        for item in workdata:
            if "【本週提醒】" in item["name"]:
                days_diff = timedefine(item["datePublished"])
                if days_diff is not None and days_diff < 8:
                    return item['description']
                
        return "國師本週還沒有提醒～"
    except json.JSONDecodeError as je:
        return None
    except KeyError as ke:
        return None
