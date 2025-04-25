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
    # 判斷是否為高星級（4星以上）
    is_highlighted = star_count >= 4
    
    return {
        "type": "box",
        "layout": "vertical",
        "backgroundColor": "#FFE4E1" if is_highlighted else colors["secondary"],
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
                        "color": "#FF6B6B" if is_highlighted else colors["text_dark"],
                        "size": "sm",
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": "★"*star_count + "☆"*(5-star_count),
                        "size": "xs",
                        "color": "#FF6B6B" if is_highlighted else colors["star"],
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
                "color": "#FF4500" if is_highlighted else colors["text_dark"]
            }
        ]
    }

def create_astro_bubble(title, star_counts, reminder):
    """創建星座運勢 Bubble"""
    
    # 生成顏色方案
    colors = generate_muted_color_scheme()
    
    # 創建運勢區塊
    fortune_boxes = []
    fortune_types = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]
    fortune_icons = ["🌟", "💝", "💼", "💰"]
    
    for i, (stars, content) in enumerate(star_counts):
        fortune_box = create_fortune_box(
            title=fortune_types[i],
            star_count=stars,
            content=content,
            icon=fortune_icons[i],
            colors=colors
        )
        fortune_boxes.append(fortune_box)

    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "size": "lg",
                    "align": "center",
                    "color": colors["text_light"],
                    "weight": "bold"
                }
            ],
            "backgroundColor": colors["primary"],
            "paddingAll": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": fortune_boxes,
            "spacing": "sm",
            "paddingAll": "md",
            "backgroundColor": colors["background"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "💫 今日小叮嚀",
                    "size": "xs",
                    "align": "center",
                    "color": colors["text_light"],
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": reminder,
                    "size": "xs",
                    "align": "center",
                    "color": colors["text_light"],
                    "wrap": True,
                    "margin": "sm"
                }
            ],
            "backgroundColor": colors["primary"],
            "paddingAll": "md"
        }
    }

