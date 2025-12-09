
import os
import json
import requests
from bs4 import BeautifulSoup
import random


#基本的抽淺草寺功能
def locat_ticket (rndNum):
    def format_result_dict(result_dict):
        formatted_results = []
        for key, value in result_dict.items():
            formatted_results.append(f"{key}：{value}")
        return "\n".join(formatted_results)
    
    # 本地讀取籤詩
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '../../', 'statics', 'light_grass_poem.json')
    with open(json_path,'r',encoding='utf-8') as fate :
        content = fate.read()
        fate_data = json.loads(content)
        choose = fate_data[rndNum]
        formatted_num = str(rndNum+1).zfill(3)
        img_url = f'https://storage.googleapis.com/linebot01/img/{formatted_num}.jpg'
        title = f'第{choose["id"]}籤'
        type = choose['type']
        poem = choose['poem']
        explain = choose['explain']
        result = format_result_dict(choose['result'])

        ticketData = [title,type,poem,explain,result],img_url

    return ticketData

#抽台北市六十甲子籤
def get_sixty_poem():
    try:
        hit = random.randint(1, 61)
        url = f"https://iwnet.civil.taipei/SignedPoetry/Home/Detail/{hit}"
        # 添加 timeout 避免請求卡住
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        poetry_div = soup.find('div', class_='main-poetry')
        if not poetry_div:
            print(f"[六十甲子籤] 找不到詩詞內容")
            return None, None

        poetry_text = poetry_div.get_text('\n', strip=True)
        process_text = [i.split('\n') for i in poetry_text.split('-')]
        process_data = []
        for i in process_text:
            for j in range(len(i)):
                process_data.append(i[j])

        res = '\n'.join(process_data)
        exp_body = soup.find('div', class_='exp-body')
        if not exp_body:
            print(f"[六十甲子籤] 找不到解說內容")
            return None, None

        CHT = exp_body.get_text()
        data = [f'第{hit}籤\n',res, '\n',CHT]

        return data, url
    except requests.exceptions.Timeout:
        print(f"[六十甲子籤] 請求超時")
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"[六十甲子籤] 網路請求錯誤: {e}")
        return None, None
    except Exception as e:
        print(f"[六十甲子籤] 發生錯誤: {e}")
        return None, None
