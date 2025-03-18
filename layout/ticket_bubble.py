def create_ticket_bubble(title, type, poem, explain, result, img_url, ai_result):
    # 將詩句按行分割
    poem_lines = poem.split('\n')
    
    # 創建詩句的 TextComponent 列表
    poem_contents = [
        {
            "type": "text",
            "text": line,
            "size": "md",
            "weight": "bold",
            "wrap": True,
            "color": "#000000",
            "margin": "sm",
            "align": "center"
        }
        for line in poem_lines
    ]
    
    flex_container = {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "2:3",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "wrap": True,
                    "color": "#1DB446"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{type}",
                            "size": "xl",
                            "wrap": True,
                            "color": "#555555",
                            "align": "center"
                        },
                        *poem_contents,  # 插入詩句內容
                        {
                            "type": "text",
                            "text": f"解釋：{explain}",
                            "size": "sm",
                            "wrap": True,
                            "color": "#555555"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": f"結果：{result}",
                    "size": "sm",
                        "weight": "bold",
                        "align": "center",
                    "wrap": True,
                    "color": "#000000"
                },
                {
                    "type": "text",
                    "text": f"露露開示：{ai_result}",
                    "size": "sm",
                    "wrap": True,
                    "color": "#555555"
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
                        "label": "取得籤詩",
                        "uri": f"{img_url}"
                    }
                }
            ],
            "flex": 0
        }
    }
    return flex_container

