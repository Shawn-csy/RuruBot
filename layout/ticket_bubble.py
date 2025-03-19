def create_ticket_bubble(title, type, poem, explain, result, img_url, ai_result):
    # 將詩句按行分割
    poem_lines = poem.split('\n')
    
    # 創建詩句的 TextComponent 列表
    poem_contents = [
        {
            "type": "text",
            "text": line,
            "size": "sm",
            "weight": "regular",
            "wrap": True,
            "color": "#555555",
            "margin": "sm",
            "align": "center"
        }
        for line in poem_lines
    ]
    
    flex_container = {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "md",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ],
            "backgroundColor": "#4A3B6B",
            "paddingAll": "md"
        },
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
            "spacing": "sm",
            "backgroundColor": "#F8F8F8",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": type,
                            "size": "md",
                            "weight": "bold",
                            "wrap": True,
                            "color": "#4A3B6B",
                            "align": "center"
                        },
                        *poem_contents
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "解釋",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": explain,
                            "size": "sm",
                            "wrap": True,
                            "color": "#555555",
                            "margin": "sm"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "結果",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": result,
                            "size": "sm",
                            "wrap": True,
                            "color": "#4A3B6B",
                            "weight": "bold",
                            "align": "center",
                            "margin": "sm"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "露露開示",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": ai_result,
                            "size": "sm",
                            "wrap": True,
                            "color": "#555555",
                            "margin": "sm"
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#4A3B6B",
            "paddingAll": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "color": "#FFFFFF",
                    "action": {
                        "type": "uri",
                        "label": "取得籤詩",
                        "uri": f"{img_url}"
                    }
                }
            ]
        }
    }
    return flex_container

