
import os
import json



#基本的抽淺草寺功能
def locat_ticket (rndNum):
    def format_result_dict(result_dict):
        formatted_results = []
        for key, value in result_dict.items():
            formatted_results.append(f"{key}：{value}")
        return "\n".join(formatted_results)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'statics', 'light_grass_poem.json')
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

