from layout.astro_bubble import create_astro_bubble
from layout.ticket_bubble import create_ticket_bubble
from linebot.v3.messaging import FlexMessage, FlexContainer
from services.gemini_reply import get_gemini_reply
import re


def process_astro_bubble_reply(data):
    
    # 檢查資料格式
    if not data or not isinstance(data, list):
        return FlexMessage(
            alt_text='今日運勢',
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "無法獲取星座資料",
                            "weight": "bold",
                            "size": "md"
                        }
                    ]
                }
            }
        )
    
    # 處理第一個元素中的多行文字
    main_content = data[0]
    content_lines = main_content.strip().split('\n')
    
    # 取得標題
    title = ""
    for line in content_lines:
        if "解析" in line or "運勢" in line:
            title = line.strip()
            break
    
    if not title and len(content_lines) > 1:
        title = content_lines[1].strip()  
    
    if not title:
        title = "今日運勢"  
    
    # 解析星級和內容
    star_counts = []
    fortune_types = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]
    
    for fortune_type in fortune_types:
        found = False
        for line in content_lines:
            if fortune_type in line:
                # 使用正則表達式提取星級和內容
                match = re.search(r'(.*?)：(.*)', line)
                if match:
                    star_part = match.group(1)
                    content_part = match.group(2)
                    
                    # 計算星星數量
                    star_count = star_part.count('★')
                    
                    star_counts.append((star_count, content_part.strip()))
                    found = True
                    break
        
        if not found:
            star_counts.append((0, "暫無資料"))
    
    # 小叮嚀（使用第二個元素或最後一行）
    reminder = ""
    if len(data) > 1 and data[1].strip():
        reminder = data[1].strip()
    elif len(content_lines) > 0 and not any(fortune_type in content_lines[-1] for fortune_type in fortune_types):
        reminder = content_lines[-1].strip()
    
    if not reminder:
        reminder = "今天也要加油喔！"
    
    # 使用新組件生成 Bubble
    astro_bubble = create_astro_bubble(
        title=title,
        star_counts=star_counts,
        reminder=reminder
    )
    
    # 將字典轉換為 FlexContainer
    flex_container = FlexContainer.from_dict(astro_bubble)
    
    flex_message = FlexMessage(
        alt_text=f'今日運勢',
        contents=flex_container
    )
    return flex_message


def process_ticket_reply(data,text):
    question = text.replace("抽淺草寺","").strip()
    title = data[0][0]
    type = data[0][1]
    poem = data[0][2]
    explain = data[0][3]
    result = data[0][4]
    img_url = data[1]

    if question:
        res = get_gemini_reply("問題 "+question+" 籤詩結果 "+title+poem+explain+result)
        ai_result = res
    else:
        ai_result = "喵？"

    ticket_bubble = create_ticket_bubble(
        title=title,
        type=type,
        poem=poem,
        explain=explain,
        result=result,
        img_url=img_url,
        ai_result=ai_result
    )

    flex_container = FlexContainer.from_dict(ticket_bubble)
    flex_message = FlexMessage(
        alt_text=f'籤詩結果',
        contents=flex_container
    )
    return flex_message
