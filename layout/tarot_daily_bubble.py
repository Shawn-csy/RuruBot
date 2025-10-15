import re
import random
import colorsys
import json
from services.features.gemini_reply import get_gemini_reply


def generate_tarot_color_scheme():
    """生成塔羅專用的神秘紫色調配色方案"""
    # 使用紫色系作為基調
    base_hue = random.uniform(0.75, 0.85)

    # 深紫色主色調 (Header/Footer)
    primary_saturation = random.uniform(0.35, 0.50)
    primary_value = random.uniform(0.30, 0.45)
    primary_rgb = colorsys.hsv_to_rgb(base_hue, primary_saturation, primary_value)
    primary_hex = "#{:02x}{:02x}{:02x}".format(
        int(primary_rgb[0] * 255),
        int(primary_rgb[1] * 255),
        int(primary_rgb[2] * 255)
    )

    # 淺紫色背景
    bg_saturation = random.uniform(0.08, 0.12)
    bg_value = random.uniform(0.96, 0.99)
    bg_rgb = colorsys.hsv_to_rgb(base_hue, bg_saturation, bg_value)
    bg_hex = "#{:02x}{:02x}{:02x}".format(
        int(bg_rgb[0] * 255),
        int(bg_rgb[1] * 255),
        int(bg_rgb[2] * 255)
    )

    # 卡片背景 (純白)
    card_bg = "#FFFFFF"

    # 重點色 (金色/紫金色)
    accent_hue = random.uniform(0.12, 0.18)  # 金色系
    accent_saturation = random.uniform(0.50, 0.70)
    accent_value = random.uniform(0.75, 0.85)
    accent_rgb = colorsys.hsv_to_rgb(accent_hue, accent_saturation, accent_value)
    accent_hex = "#{:02x}{:02x}{:02x}".format(
        int(accent_rgb[0] * 255),
        int(accent_rgb[1] * 255),
        int(accent_rgb[2] * 255)
    )

    return {
        "primary": primary_hex,
        "background": bg_hex,
        "card_bg": card_bg,
        "accent": accent_hex,
        "text_dark": "#2C2C2C",
        "text_light": "#FFFFFF",
        "text_muted": "#757575",
        "text_content": "#424242",
        "divider": "#E0E0E0"
    }


def create_tarot_daily_bubble(tarot_data: str):
    """
    建立每日塔羅的 Flex Message Bubble

    Args:
        tarot_data: API 返回的每日塔羅文字內容

    Returns:
        dict: Flex Message Bubble 格式
    """

    # 生成配色方案
    colors = generate_tarot_color_scheme()

    # 使用 AI 解析塔羅資料
    parsed_data = _parse_tarot_with_ai(tarot_data)

    # 建立運勢區塊列表
    fortune_contents = []

    # 添加愛情運
    if parsed_data.get("love"):
        fortune_contents.append(_create_fortune_card(
            "💞",
            "愛情運",
            parsed_data["love"],
            colors
        ))

    # 添加事業運
    if parsed_data.get("career"):
        fortune_contents.append(_create_fortune_card(
            "💼",
            "事業運",
            parsed_data["career"],
            colors
        ))

    # 添加財運
    if parsed_data.get("finance"):
        fortune_contents.append(_create_fortune_card(
            "💰",
            "財運",
            parsed_data["finance"],
            colors
        ))

    # 添加整體運勢
    if parsed_data.get("overall"):
        fortune_contents.append(_create_overall_card(
            parsed_data["overall"],
            colors
        ))

    # 建立 Bubble 結構
    bubble = {
        "type": "bubble",
        "size": "giga",  # 使用最寬的版面
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔮",
                            "size": "xl",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": "今日塔羅運勢",
                            "size": "lg",
                            "weight": "bold",
                            "color": colors["text_light"],
                            "margin": "sm",
                            "flex": 1
                        }
                    ],
                    "alignItems": "center"
                }
            ],
            "backgroundColor": colors["primary"],
            "paddingAll": "lg"  # md → lg: 增加 header 內距
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": fortune_contents,
            "spacing": "md",  # sm → md: 增加卡片間距
            "paddingAll": "lg",  # md → lg: 增加 body 內距
            "backgroundColor": colors["background"]
        }
    }

    # 如果有今日訊息,添加 footer
    if parsed_data.get("message"):
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "✨",
                            "size": "md",
                            "flex": 0
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "今日訊息",
                                    "size": "sm",  # xs → sm: 增加標題大小
                                    "weight": "bold",
                                    "color": colors["text_light"]
                                },
                                {
                                    "type": "text",
                                    "text": parsed_data["message"],
                                    "size": "xs",  # xxs → xs: 增加內容大小
                                    "color": colors["text_light"],
                                    "wrap": True,
                                    "margin": "sm",  # xs → sm: 增加間距
                                    "action": {
                                        "type": "clipboard",
                                        "clipboardText": parsed_data["message"]
                                    }
                                }
                            ],
                            "margin": "sm"
                        }
                    ]
                }
            ],
            "backgroundColor": colors["primary"],
            "paddingAll": "lg"  # md → lg: 增加 footer 內距
        }

    return bubble


def _create_fortune_card(emoji: str, title: str, fortune_data: dict, colors: dict):
    """
    建立精美的運勢卡片

    Args:
        emoji: 運勢類別的 emoji
        title: 運勢類別標題
        fortune_data: 運勢資料
        colors: 配色方案

    Returns:
        dict: 運勢卡片的 box
    """

    card = fortune_data.get("card", "未知")
    position = fortune_data.get("position", "正位")
    content = fortune_data.get("content", "")
    advice = fortune_data.get("advice", "保持正向心態。")

    # 決定位置的標記和顏色
    is_upright = "正位" in position
    position_mark = "⬆" if is_upright else "⬇"
    position_color = "#66BB6A" if is_upright else "#EF5350"

    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            # 卡片標題區
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": emoji,
                                "size": "xl",  # lg → xl: 增加 emoji 大小
                                "align": "center"
                            }
                        ],
                        "width": "36px",  # 32px → 36px: 增加圖示區塊
                        "height": "36px",
                        "backgroundColor": colors["background"],
                        "cornerRadius": "md",
                        "justifyContent": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "weight": "bold",
                                "size": "lg",  # md → lg: 增加標題大小
                                "color": colors["text_dark"]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": card,
                                        "size": "xs",  # xxs → xs: 增加牌名大小
                                        "color": colors["text_muted"],
                                        "flex": 0
                                    },
                                    {
                                        "type": "text",
                                        "text": f" {position_mark} {position}",
                                        "size": "xs",  # xxs → xs: 增加位置標示大小
                                        "color": position_color,
                                        "weight": "bold",
                                        "flex": 0
                                    }
                                ],
                                "margin": "sm"  # xs → sm: 增加間距
                            }
                        ],
                        "margin": "sm"
                    }
                ],
                "paddingBottom": "sm"
            },
            # 分隔線
            {
                "type": "separator",
                "color": colors["divider"]
            },
            # 內容區
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": content,
                        "size": "sm",  # xs → sm: 增加內容文字大小
                        "color": colors["text_content"],
                        "wrap": True,
                        "lineSpacing": "6px",  # 4px → 6px: 增加行距
                        "action": {
                            "type": "clipboard",
                            "clipboardText": content
                        }
                    }
                ],
                "paddingTop": "md",  # sm → md: 增加上內距
                "paddingBottom": "sm"  # xs → sm: 增加下內距
            },
            # 建議區
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "filler"
                            }
                        ],
                        "width": "4px",  # 3px → 4px: 增加裝飾條寬度
                        "backgroundColor": colors["accent"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡 建議",
                                "size": "xs",  # xxs → xs: 增加建議標題大小
                                "color": colors["accent"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": advice,
                                "size": "xs",  # xxs → xs: 增加建議內容大小
                                "color": colors["text_muted"],
                                "wrap": True,
                                "margin": "sm",  # xs → sm: 增加間距
                                "action": {
                                    "type": "clipboard",
                                    "clipboardText": advice
                                }
                            }
                        ],
                        "margin": "sm"  # xs → sm: 增加左邊距
                    }
                ],
                "paddingAll": "sm",  # xs → sm: 增加建議區內距
                "backgroundColor": "#FAFAFA",
                "cornerRadius": "sm"
            }
        ],
        "backgroundColor": colors["card_bg"],
        "cornerRadius": "xl",  # lg → xl: 增加圓角,更柔和
        "paddingAll": "lg",  # md → lg: 增加卡片內距
        "borderWidth": "medium",  # 1px → medium: 增加邊框粗細,更明顯
        "borderColor": colors["divider"]
    }


def _create_overall_card(overall_text: str, colors: dict):
    """
    建立整體運勢卡片

    Args:
        overall_text: 整體運勢內容
        colors: 配色方案

    Returns:
        dict: 整體運勢卡片的 box
    """

    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            # 標題
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "🌟",
                        "size": "xl",  # lg → xl: 增加 emoji 大小
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "整體運勢",
                        "weight": "bold",
                        "size": "lg",  # md → lg: 增加標題大小
                        "color": colors["text_dark"],
                        "margin": "sm"
                    }
                ],
                "paddingBottom": "md"  # sm → md: 增加底部間距
            },
            # 分隔線
            {
                "type": "separator",
                "color": colors["divider"]
            },
            # 內容
            {
                "type": "text",
                "text": overall_text,
                "size": "sm",  # xs → sm: 增加文字大小
                "color": colors["text_content"],
                "wrap": True,
                "lineSpacing": "6px",  # 4px → 6px: 增加行距
                "margin": "md",  # sm → md: 增加上邊距
                "action": {
                    "type": "clipboard",
                    "clipboardText": overall_text
                }
            }
        ],
        "backgroundColor": colors["card_bg"],
        "cornerRadius": "xl",  # lg → xl: 增加圓角,更柔和
        "paddingAll": "lg",  # md → lg: 增加卡片內距
        "borderWidth": "medium",  # 1px → medium: 增加邊框粗細,更明顯
        "borderColor": colors["divider"]
    }


def _parse_tarot_with_ai(tarot_data: str) -> dict:
    """
    使用 AI 解析塔羅 Markdown 內容為結構化 JSON

    Args:
        tarot_data: 原始塔羅 Markdown 內容

    Returns:
        dict: 結構化的塔羅資料
    """

    system_prompt = """你是一個專門解析塔羅占卜結果的助手。
你的任務是將 Markdown 格式的塔羅內容轉換成結構化的 JSON 格式,方便程式處理。

**重要規則**:
1. 不要修改、總結或改寫原始內容
2. 保留所有原文,包括標點符號
3. 只做分類和結構化工作
4. 以 Markdown 的 **文字** 標記作為分段依據

**輸出格式** (必須是有效的 JSON):
{
  "love": {
    "card": "塔羅牌名稱",
    "position": "正位或逆位",
    "content": "完整的運勢內容(不包含建議)",
    "advice": "建議內容"
  },
  "career": {
    "card": "塔羅牌名稱",
    "position": "正位或逆位",
    "content": "完整的運勢內容(不包含建議)",
    "advice": "建議內容"
  },
  "finance": {
    "card": "塔羅牌名稱",
    "position": "正位或逆位",
    "content": "完整的運勢內容(不包含建議)",
    "advice": "建議內容"
  },
  "overall": "整體運勢的完整內容",
  "message": "今日訊息的完整內容"
}

**如何識別各個部分**:
- 愛情運: 以 💞 **愛情運** 開頭
- 事業運: 以 💼 **事業運** 開頭
- 財運: 以 💰 **財運** 開頭
- 整體運勢: 以 🌟 **整體運勢** 開頭
- 今日訊息: 以 ✨ **今日訊息** 開頭

**建議的識別**:
- 尋找 **建議** 關鍵字後面的內容
- 如果沒有明確的建議標記,則將最後一句包含建議性詞彙(不妨、可以、建議、試著、記得、保持、避免、注意)的句子作為建議

只回傳 JSON,不要有其他說明文字。
"""

    prompt = f"""請將以下塔羅占卜內容轉換成 JSON 格式:

{tarot_data}
"""

    try:
        ai_response = get_gemini_reply(prompt, system_prompt)

        # 清理 AI 回應,移除可能的 markdown 代碼塊標記
        ai_response = ai_response.strip()
        if ai_response.startswith("```json"):
            ai_response = ai_response[7:]
        if ai_response.startswith("```"):
            ai_response = ai_response[3:]
        if ai_response.endswith("```"):
            ai_response = ai_response[:-3]
        ai_response = ai_response.strip()

        # 解析 JSON
        parsed_data = json.loads(ai_response)
        return parsed_data

    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}")
        print(f"AI 回應: {ai_response}")
        # 回傳空結構
        return {
            "love": None,
            "career": None,
            "finance": None,
            "overall": None,
            "message": None
        }
    except Exception as e:
        print(f"AI 解析錯誤: {e}")
        # 回傳空結構
        return {
            "love": None,
            "career": None,
            "finance": None,
            "overall": None,
            "message": None
        }
