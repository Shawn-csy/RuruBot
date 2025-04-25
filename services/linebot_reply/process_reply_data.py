from layout.astro_bubble import create_astro_bubble
from layout.ticket_bubble import create_ticket_bubble
from layout.podcast_bubble import create_podcast_bubble
from linebot.v3.messaging import FlexMessage, FlexContainer
from services.features.gemini_reply import get_gemini_reply
from layout.general_poem_bubble import create_general_poem_bubble
from layout.help_bubble import create_help_bubble
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

def process_podcast_reply(data):
    # 確保資料是字串
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    
    if not isinstance(data, str):
        
        return FlexMessage(
            alt_text='本週星座運勢',
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "無法解析星座運勢資料",
                            "weight": "bold"
                        }
                    ]
                }
            })
        )
    
    # 解析標題和日期
    lines = data.strip().split('\n')
    title = lines[0].strip()
    
    # 初始化運勢分類
    fortune_groups = {
        "累的": [],
        "穩的": [],
        "讚的": []
    }
    
    current_group = None
    
    # 解析各星座運勢
    for line in lines:
        line = line.strip()
        # 跳過空行
        if not line:
            continue
        
        # 檢查是否是分類標題
        if "【" in line and "】" in line:
            for group in fortune_groups.keys():
                if group in line:
                    current_group = group
                    break
            continue
        
        # 解析星座運勢
        if current_group and "：" in line:
            parts = line.split("：", 1)
            if len(parts) == 2:
                sign, fortune = parts
                fortune_groups[current_group].append({
                    "sign": sign.strip(),
                    "fortune": fortune.strip()
                })
        
    
    # 使用 create_podcast_bubble 創建 bubble
    bubble = create_podcast_bubble(title, fortune_groups)
    
    return FlexMessage(
        alt_text='本週星座運勢',
        contents=FlexContainer.from_dict(bubble)
    )

def process_sixty_poem_reply(data, url, text):
    # 處理標題
    poem_name = "六十甲子籤"
    title = data[0].strip()
    poem = data[1].strip()
    explain = data[3].strip()

    result = get_gemini_reply("問題 "+text+" 籤詩結果 "+title+poem+explain)
    web_url = url
    img_url = None  # 或設置一個預設圖片
    
    return FlexMessage(
        alt_text='六十甲子籤',
        contents=FlexContainer.from_dict(
            create_general_poem_bubble(
                poem_name=poem_name,
                title=title,
                poem=poem,
                explain=explain,
                result=result,
                img_url=img_url,  # 添加缺少的參數
                web_url=web_url
            )
        )
    )


def process_help_reply(data):
    bubble = create_help_bubble(data)
    flex_message = FlexMessage(
        alt_text="使用說明",
        contents=FlexContainer.from_dict(bubble)
    )
    
    return flex_message

async def process_text_message(event):
    """處理文字訊息"""
    user_id = event.source.user_id
    message = event.message.text
    
    # 使用更新後的 get_gemini_reply
    response = await get_gemini_reply(message, user_id)
    
    if response:
        return response
    return None

