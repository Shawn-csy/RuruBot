from services.features.command_ai import parse_command_with_ai
from services.constants import astro as astro_dict
from utils.tool import dice_pattern

def parse_command(text):
    """解析用戶輸入的命令和參數"""
    # 先嘗試使用傳統方式解析
    command, params = parse_command_traditional(text)
    
    # 如果傳統方式無法解析，使用 AI 解析
    if not command:
        command, params = parse_command_with_ai(text)
    
    return command, params
    


def parse_command_traditional(text):
    """傳統的命令解析方法"""
    #雷達功能
    if "雷達" in text or "radar" in text.lower():
        return "radar", {}
    #星座功能,用-w 取每周星座, 不加-w 取每日星座
    if "-w" in text and text.replace("-w", "").strip() in astro_dict:
        text = text.replace("-w", "").strip()
        return "astro", {"astro_name": text, "type": "weekly"}
    elif text in astro_dict:
        return "astro", {"astro_name": text, "type": "daily"}
    # #骰子功能
    # elif text == "風險骰子":
    #     return "risk_dice", {}
    # elif "擲骰子" in text or "骰子" in text:
    #     return "random_dice", {"type": text}
    # elif "擲骰" in text or "骰" in text or dice_pattern.match(text):
    #     return "random_dice", {"type": text}
    #籤詩功能
    elif "抽淺草寺" in text:
        return "ticket", {"text": text}
    elif "抽六十甲子籤" in text:
        return "sixty_poem", {"text": text.replace("抽六十甲子籤", "").strip()}
    #國師功能
    elif "本週國師" in text:
        return "podcast", {}
    elif "--help" in text:
        return "help", {}
    #如果沒有匹配到任何命令，返回 None
    return None, {}
    