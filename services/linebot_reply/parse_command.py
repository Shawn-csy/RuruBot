from services.constants import astro as astro_dict
from utils.tool import dice_pattern

def parse_command(text):
    """解析用戶輸入的命令和參數"""
    #雷達功能
    if "雷達" in text or "radar" in text.lower():
        return "radar", {}
    #星座功能,用-w 取每周星座, 不加-w 取每日星座
    if "-w" in text and text.replace("-w", "").strip() in astro_dict:
        text = text.replace("-w", "").strip()
        return "astro", {"astro_name": text, "type": "weekly"}
    elif "風險骰子" == text:
        return "risk_dice", {}
    elif "擲骰子" in text or "骰子" in text:
        return "random_dice", {"type": text}
    elif "擲骰" or "骰" or dice_pattern.match(text):
        return "random_dice", {"type": text}
    
    elif text in astro_dict:
        return "astro", {"astro_name": text, "type": "daily"}
    #籤詩功能
    elif "抽淺草寺" in text:
        return "ticket", {"text": text}
    #國師功能
    elif "本週國師" in text:
        return "podcast", {}
    