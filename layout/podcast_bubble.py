from services.constants import astro_icons

def create_podcast_bubble(title, fortune_groups):
    bubble = {
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
                    "wrap": True,
                    "size": "sm",
                    "color": "#FFFFFF"
                }
            ],
            "backgroundColor": "#4A3B6B",
            "paddingAll": "sm"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "backgroundColor": "#F8F8F8",
            "paddingAll": "md",
            "spacing": "sm"
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
                        "label": "造訪國師",
                        "uri": f"https://podcasts.apple.com/tw/podcast/%E5%94%90%E9%99%BD%E9%9B%9E%E9%85%92%E5%B1%8B/id1536374746"
                    }
                }
            ]
        }
    }
    
    # 定義三種運勢的顏色
    colors = {
        "累的": "#D88A8A",
        "穩的": "#8AAD8A",
        "讚的": "#8A8AC5"
    }
    
    # 添加各分類的運勢
    for group, fortunes in fortune_groups.items():
        group_box = {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "cornerRadius": "md",
            "paddingAll": "md",
            "margin": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f"【{group}】",
                    "weight": "bold",
                    "size": "sm",
                    "color": colors[group]
                }
            ],
            
        }
        
        # 添加該分類下的星座運勢
        for fortune in fortunes:
            sign = fortune["sign"]+"座"
            icon = astro_icons.get(sign, "⭐")
            
            group_box["contents"].append({
                "type": "box",
                "layout": "vertical",
                "margin": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": icon,
                                "size": "sm",
                                "flex": 0,
                                "color": colors[group]
                            },
                            {
                                "type": "text",
                                "text": sign,
                                "weight": "bold",
                                "size": "sm",
                                "color": "#555555",
                                "margin": "sm"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": fortune["fortune"],
                        "wrap": True,
                        "size": "xs",
                        "color": "#555555",
                        "margin": "sm"
                    }
                ]
            })
        
        bubble["body"]["contents"].append(group_box)
    
    return bubble