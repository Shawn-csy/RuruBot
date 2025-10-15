from services.features.command_ai import parse_command_with_ai
from services.constants import astro as astro_dict, command_patterns
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
    #音樂推薦功能
    elif "--m"  in text:
        return "music", {}
    #指定用戶音樂推薦功能
    elif "--ping" in text:
        user_name = text.replace("--ping", "").strip()
        if user_name:
            return "music", {"user_name": user_name}
        else:
            return "music", {}
    #露露 AI 對話功能
    elif text.startswith("露露"):
        content = text[2:].strip()  # 移除「露露」並去除空白
        if content:  # 確保有內容
            return "lulu_chat", {"text": content}

    # ==================== 塔羅牌占卜功能（新版 API） ====================

    # 每日塔羅
    elif text == "每日塔羅" or "本日塔羅":
        return "tarot", {"method": "daily", "question": None}

    # 問題塔羅：-塔羅 [問題]
    elif text.startswith("-塔羅"):
        question = text[3:].strip()  # 移除 "-塔羅" 並取得問題
        if question:  # 確保有問題內容
            return "tarot", {"method": "question", "question": question}
        else:
            # 如果只輸入 "-塔羅" 沒有問題，則視為每日塔羅
            return "tarot", {"method": "daily", "question": None}

    # ==================== 舊版塔羅功能（已註解） ====================
    # # 塔羅牌占卜說明（必須在塔羅占卜之前檢查，避免衝突）
    # elif text in ["-塔羅說明", "--tarot-help", "-塔羅幫助", "--tarot help"]:
    #     return "tarot_help", {}

    # # 塔羅牌占卜功能（需要明確指令）
    # elif (text.startswith("-塔羅") or text.startswith("--tarot")) and text not in ["-塔羅說明", "-塔羅幫助"]:
    #     # 解析問題和牌陣
    #     question = None
    #     spread_name = "時間之流占卜法"  # 預設牌陣

    #     # 移除關鍵字，提取問題
    #     if text.startswith("-塔羅"):
    #         cleaned_text = text[3:].strip()  # 移除 "-塔羅"
    #     else:
    #         cleaned_text = text[7:].strip()  # 移除 "--tarot"

    #     # 檢查是否指定牌陣
    #     spread_keywords = {
    #         "時間之流": "時間之流占卜法",
    #         "問題解決": "問題解決占卜法 / 問題解決牌陣",
    #         "四要素": "要素展開法 / 四要素展開法",
    #         "塞爾特": "塞爾特十字占卜法（塞爾特十字牌陣）",
    #         "馬蹄鐵": "Ｖ字形馬蹄鐵占卜法",
    #         "靈感對應": "靈感對應牌陣 / 靈感對應占卜法",
    #         "二擇一": "二擇一占卜法",
    #         "三擇一": "三擇一牌陣 / 三擇一占卜法"
    #     }

    #     for keyword, spread in spread_keywords.items():
    #         if keyword in cleaned_text:
    #             spread_name = spread
    #             cleaned_text = cleaned_text.replace(keyword, "").strip()
    #             break

    #     # 剩餘的文字作為問題
    #     if cleaned_text:
    #         question = cleaned_text

    #     return "tarot", {"question": question, "spread_name": spread_name}

    #如果沒有匹配到任何命令，返回 None
    return None, {}
    