def create_general_poem_bubble(poem_name, title, poem, explain, result, img_url, web_url):
    # 將詩句按行分割
    poem_lines = poem.split('\n')
    
    # 創建詩句的 TextComponent 列表
    poem_contents = []
    # 添加標題
    poem_contents.append({
        "type": "text",
        "text": title,
        "size": "sm",
        "weight": "regular",
        "wrap": True,
        "color": "#555555",
        "margin": "sm",
        "align": "center"
    })
    
    # 添加每一行詩句
    for line in poem_lines:
        poem_contents.append({
            "type": "text",
            "text": line,
            "color": "#555555",
            "margin": "sm",
            "align": "center"
        })

    # 設置 hero 圖片
    if img_url:
        hero = {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectRatio": "2:3",
            "aspectMode": "cover"
        }
    else:
        hero = None

    # 創建基本容器
    flex_container = {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": poem_name,
                    "weight": "bold",
                    "size": "md",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ],
            "backgroundColor": "#4A3B6B",
            "paddingAll": "md"
        }
    }
    
    # 如果有圖片，添加 hero 部分
    if hero:
        flex_container["hero"] = hero
        
    # 繼續添加其他部分
    flex_container.update({
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
                            "text": "籤詩",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "weight": "bold"
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
                        "uri": f"{web_url}"
                    }
                }
            ]
        }
    })
    return flex_container
    

