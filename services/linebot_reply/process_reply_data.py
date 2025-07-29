from layout.astro_bubble import create_astro_bubble
from layout.ticket_bubble import create_ticket_bubble
from layout.podcast_bubble import create_podcast_bubble
from linebot.v3.messaging import FlexMessage, FlexContainer
from services.features.gemini_reply import get_gemini_reply
from layout.general_poem_bubble import create_general_poem_bubble
from layout.help_bubble import create_help_bubble
import re
from typing import Dict, Any



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
        print("資料不是字串類型")
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
    print(f"解析後的行數: {len(lines)}")

    
    # 提取完整的標題（可能包含多行）
    title = ""
    title_lines = []
    

    for i, line in enumerate(lines):
        line = line.strip()

        if line.startswith("【本週提醒】"):
            # 找到【本週提醒】開頭的行
            title_lines.append(line)
      
            # 檢查下一行是否也是標題的一部分（不包含【】）
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith("【"):
                title_lines.append(lines[j].strip())
        
                j += 1
            break
    
    if title_lines:
        title = " ".join(title_lines)
     
    else:
        title = lines[0].strip() if lines else "【本週提醒】"
      
    
    # 在【本週提醒】後面增加換行
    if "【本週提醒】" in title:
        # 找到【本週提醒】的位置
        reminder_pos = title.find("【本週提醒】")
        if reminder_pos != -1:
            # 在【本週提醒】後面插入換行
            title = title[:reminder_pos + len("【本週提醒】")] + "\n" + title[reminder_pos + len("【本週提醒】"):]
    
    print(f"最終標題: '{title}'")
    
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


def process_music_reply(data: Dict[str, Any]) -> FlexMessage:
    """處理音樂推薦的回覆"""
    try:
        # 計算播放時間（分鐘:秒）
        duration_seconds = data["duration_ms"] // 1000
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        duration_str = f"{minutes}:{seconds:02d}"
        
        # 建立音樂資訊的 bubble
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": data.get("image_url", "https://via.placeholder.com/1024x400?text=No+Image"),
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": data["name"],
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": data["artist"],
                        "color": "#666666",
                        "size": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "專輯",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": data["album"],
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 4
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "類型",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": data["genre"],
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 4
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "時長",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": duration_str,
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 4
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱門度",
                                        "color": "#aaaaaa",
                                        "size": "sm",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{data['popularity']}/100",
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 4
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "在 Spotify 聆聽",
                            "uri": data["external_url"]
                        }
                    }
                ]
            }
        }
        
        # 如果有預覽 URL，添加預覽按鈕
        if data.get("preview_url"):
            bubble["footer"]["contents"].append({
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "uri",
                    "label": "試聽",
                    "uri": data["preview_url"]
                }
            })
            
        return FlexMessage(
            alt_text=f"音樂推薦: {data['name']} - {data['artist']}",
            contents=FlexContainer.from_dict(bubble)
        )
        
    except Exception as e:
        print(f"處理音樂回覆時發生錯誤: {str(e)}")
        return FlexMessage(
            alt_text="音樂推薦",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "無法顯示音樂資訊",
                            "weight": "bold"
                        }
                    ]
                }
            })
        )

