def create_help_bubble(content):
    """建立幫助訊息的 Bubble"""
    bubble = {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": content["title"],
                    "weight": "bold",
                    "size": "xl",
                    "color": "#ffffff",
                    "align": "center"
                }
            ],
            "backgroundColor": "#4A3B6B",
            "paddingAll": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "spacing": "md",
            "paddingAll": "md"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": content["footer"]["text"],
                    "wrap": True,
                    "color": "#ffffff",
                    "size": "sm",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": content["footer"]["note"],
                    "wrap": True,
                    "color": "#ffffff",
                    "size": "xs",
                    "margin": "sm",
                    "align": "center"
                }
            ],
            "backgroundColor": "#4A3B6B",
            "paddingAll": "md"
        }
    }

    # 添加每個功能區塊
    for i in range(0, len(content["sections"]), 2):
        # 創建水平容器
        row_box = {
            "type": "box",
            "layout": "horizontal",
            "contents": [],
            "spacing": "md"
        }

        # 添加左側功能區塊
        left_section = content["sections"][i]
        left_box = create_section_box(left_section)
        row_box["contents"].append(left_box)

        # 如果還有右側功能區塊，也添加進去
        if i + 1 < len(content["sections"]):
            right_section = content["sections"][i + 1]
            right_box = create_section_box(right_section)
            row_box["contents"].append(right_box)

        bubble["body"]["contents"].append(row_box)

    return bubble

def create_section_box(section):
    """創建單個功能區塊"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            # 標題
            {
                "type": "text",
                "text": section["title"],
                "weight": "bold",
                "size": "md",
                "color": "#4A3B6B"
            },
            # 指令列表
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔸",
                                "size": "xs",
                                "color": "#666666",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": cmd,
                                "size": "xs",
                                "color": "#666666",
                                "flex": 1,
                                "margin": "sm"
                            }
                        ],
                        "spacing": "sm"
                    } for cmd in section["commands"]
                ],
                "margin": "sm",
                "spacing": "sm"
            },
            # 說明文字
            {
                "type": "text",
                "text": section["description"],
                "size": "xxs",
                "color": "#aaaaaa",
                "margin": "sm",
                "wrap": True
            }
        ],
        "backgroundColor": "#ffffff",
        "cornerRadius": "md",
        "paddingAll": "md",
        "margin": "sm",
        "flex": 1
    } 