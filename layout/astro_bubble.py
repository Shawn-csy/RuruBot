
import random
import colorsys

def generate_muted_color_scheme():
    """生成低彩度的顏色方案"""
    # 基礎色調 - 隨機選擇色相 (0-1)
    base_hue = random.random()
    
    # 低彩度的主色調 (用於標題和頁腳)
    primary_saturation = random.uniform(0.2, 0.4)  # 較低的飽和度
    primary_value = random.uniform(0.2, 0.4)  # 較低的亮度值
    primary_rgb = colorsys.hsv_to_rgb(base_hue, primary_saturation, primary_value)
    primary_hex = "#{:02x}{:02x}{:02x}".format(
        int(primary_rgb[0] * 255),
        int(primary_rgb[1] * 255),
        int(primary_rgb[2] * 255)
    )
    
    # 次要色調 (用於運勢區塊背景)
    secondary_saturation = random.uniform(0.05, 0.15)  # 更低的飽和度
    secondary_value = random.uniform(0.85, 0.95)  # 較高的亮度值
    secondary_rgb = colorsys.hsv_to_rgb(base_hue, secondary_saturation, secondary_value)
    secondary_hex = "#{:02x}{:02x}{:02x}".format(
        int(secondary_rgb[0] * 255),
        int(secondary_rgb[1] * 255),
        int(secondary_rgb[2] * 255)
    )
    
    # 背景色調 (用於主體背景)
    bg_saturation = random.uniform(0.05, 0.1)  # 非常低的飽和度
    bg_value = random.uniform(0.9, 0.98)  # 非常高的亮度值
    bg_rgb = colorsys.hsv_to_rgb(base_hue, bg_saturation, bg_value)
    bg_hex = "#{:02x}{:02x}{:02x}".format(
        int(bg_rgb[0] * 255),
        int(bg_rgb[1] * 255),
        int(bg_rgb[2] * 255)
    )
    
    # 邊框色調 (用於運勢區塊邊框)
    border_saturation = random.uniform(0.1, 0.2)
    border_value = random.uniform(0.7, 0.8)
    border_rgb = colorsys.hsv_to_rgb(base_hue, border_saturation, border_value)
    border_hex = "#{:02x}{:02x}{:02x}".format(
        int(border_rgb[0] * 255),
        int(border_rgb[1] * 255),
        int(border_rgb[2] * 255)
    )
    
    # 星星色調 (用於星星)
    star_hue = (base_hue + random.uniform(0.05, 0.15)) % 1.0  # 稍微偏移的色相
    star_saturation = random.uniform(0.4, 0.6)
    star_value = random.uniform(0.6, 0.8)
    star_rgb = colorsys.hsv_to_rgb(star_hue, star_saturation, star_value)
    star_hex = "#{:02x}{:02x}{:02x}".format(
        int(star_rgb[0] * 255),
        int(star_rgb[1] * 255),
        int(star_rgb[2] * 255)
    )
    
    return {
        "primary": primary_hex,      # 標題和頁腳背景
        "secondary": secondary_hex,  # 運勢區塊背景
        "background": bg_hex,        # 主體背景
        "border": border_hex,        # 運勢區塊邊框
        "star": star_hex,            # 星星顏色
        "text_dark": "#333333",      # 深色文字
        "text_light": "#FFFFFF"      # 淺色文字
    }

def create_fortune_box(title, star_count, content, icon, colors):
    """生成單個運勢區塊"""
    return {
        "type": "box",
        "layout": "vertical",
        "backgroundColor": colors["secondary"],
        "cornerRadius": "md",
        "paddingAll": "sm",
        "borderWidth": "1px",
        "borderColor": colors["border"],
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{icon} {title}",
                        "weight": "bold",
                        "color": colors["text_dark"],
                        "size": "sm",
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": "★"*star_count + "☆"*(5-star_count),
                        "size": "xs",
                        "color": colors["star"],
                        "flex": 2,
                        "align": "end"
                    }
                ]
            },
            {
                "type": "text",
                "text": content,
                "size": "xs",
                "wrap": True,
                "margin": "sm",
                "color": colors["text_dark"]
            }
        ]
    }

def create_astro_bubble(title, star_counts, reminder, starreminder=None):
    """創建星座運勢 Bubble，使用隨機生成的低彩度顏色"""
    # 生成顏色方案
    colors = generate_muted_color_scheme()
    
    fortune_icons = ["🎯", "💝", "💼", "💰"]
    fortune_titles = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]
    
    # 創建運勢區塊
    fortune_boxes = []
    for i, (star_count, content) in enumerate(star_counts):
        if i < len(fortune_titles) and i < len(fortune_icons):
            fortune_box = create_fortune_box(
                fortune_titles[i], 
                star_count, 
                content, 
                fortune_icons[i],
                colors
            )
            fortune_boxes.append(fortune_box)
    
    # 創建頁腳內容
    footer_contents = []
    
    # 如果有速配星座，添加速配星座區塊
    if starreminder:
        footer_contents.extend([
            {
                "type": "text",
                "text": "💫 速配星座",
                "weight": "bold",
                "color": colors["text_light"],
                "size": "xs",
                "align": "center"
            },
            {
                "type": "text",
                "text": starreminder,
                "color": colors["text_light"],
                "size": "xs",
                "wrap": True,
                "align": "center",
                "margin": "sm"
            }
        ])

    # 添加提醒區塊
    footer_contents.extend([
        {
            "type": "text",
            "text": "💫 " + ("每週提醒" if starreminder else "今日小叮嚀"),
            "weight": "bold",
            "color": colors["text_light"],
            "size": "xs",
            "align": "center",
            "margin": "md" if starreminder else None
        },
        {
            "type": "text",
            "text": reminder,
            "color": colors["text_light"],
            "size": "xs",
            "wrap": True,
            "align": "center",
            "margin": "sm"
        }
    ])

    # 創建 Bubble 容器
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "md",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg",
                    "color": colors["text_light"],
                    "align": "center"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["background"],
            "paddingAll": "md",
            "spacing": "sm",
            "contents": fortune_boxes
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "md",
            "contents": footer_contents
        }
    }
    
    return bubble

