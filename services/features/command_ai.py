from services.constants import command_prompt, astro, command_patterns
from services.features.gemini_reply import get_gemini_reply
import json
import re

def parse_command_with_ai(text: str) -> tuple:
    """使用 AI 解析用戶指令"""
    try:
        # 先進行關鍵字匹配
        if not _has_valid_keywords(text):
            return None, {}
            
        # 組合提示詞
        prompt = f"{command_prompt}\n用戶輸入: {text}"
        
        # 獲取 AI 回應
        response = get_gemini_reply(prompt)
        
        # 清理回應（移除可能的額外文字）
        response = re.search(r'\{.*\}', response)
        if not response:
            return None, {}
            
        # 解析 JSON 回應
        result = json.loads(response.group())
        
        # 驗證回應格式和內容
        command, params = _validate_and_clean_response(result, text)
        if not command:
            return None, {}
            
        return command, params
        
    except Exception as e:
        print(f"AI 指令解析錯誤: {str(e)}")
        return None, {}

def _has_valid_keywords(text: str) -> bool:
    """檢查文本是否包含有效的關鍵字"""
    # 檢查是否包含任何命令的關鍵字
    for command, patterns in command_patterns.items():
        if isinstance(patterns, list):
            if any(keyword in text for keyword in patterns):
                return True
        elif isinstance(patterns, dict):
            # 對於 astro 這樣的特殊情況
            if command == "astro":
                basic_patterns = patterns.get("patterns", [])
                weekly_patterns = patterns.get("weekly_patterns", [])
                signs = patterns.get("signs", {})
                if (any(keyword in text for keyword in basic_patterns) or
                    any(keyword in text for keyword in weekly_patterns) or
                    any(sign in text for sign in signs)):
                    return True
    return False

def _validate_and_clean_response(result: dict, original_text: str) -> tuple:
    """驗證並清理 AI 回應"""
    if not isinstance(result, dict):
        return None, {}
        
    if "command" not in result or "params" not in result:
        return None, {}
        
    command = result["command"]
    params = result["params"]

    # 如果 AI 回傳 null，表示無法識別指令
    if command is None:
        return None, {}

    # 檢查 command 是否為有效值
    valid_commands = {"radar", "astro", "ticket", "sixty_poem", "podcast", "help", "music", "lulu_chat"}
    if command not in valid_commands:
        return None, {}
        
    # 根據不同命令進行特定驗證
    if command == "astro":
        if not _validate_astro_command(params, original_text):
            return None, {}
            
    elif command == "ticket":
        if not _validate_ticket_command(params, original_text):
            return None, {}
            
    elif command == "sixty_poem":
        if not _validate_sixty_poem_command(params, original_text):
            return None, {}

    elif command == "lulu_chat":
        if not _validate_lulu_chat_command(params, original_text):
            return None, {}

    # 驗證命令關鍵字是否真的出現在原文中
    if not _validate_command_keywords(command, original_text):
        return None, {}

    return command, params

def _validate_astro_command(params: dict, text: str) -> bool:
    """驗證星座命令的參數"""
    if "astro_name" not in params or "type" not in params:
        return False
        
    # 檢查星座名稱是否有效
    if params["astro_name"] not in astro:
        return False
        
    # 檢查類型是否有效
    if params["type"] not in ["daily", "weekly"]:
        return False
        
    # 確保原文中確實包含星座相關關鍵字
    keywords = command_patterns["astro"]["patterns"]
    weekly_keywords = command_patterns["astro"]["weekly_patterns"]
    
    # 檢查是否包含星座名稱
    if params["astro_name"] not in text:
        return False
        
    # 檢查是否包含運勢相關關鍵字
    if not any(keyword in text for keyword in keywords):
        return False
        
    # 如果是週運勢，檢查是否包含週運勢關鍵字
    if params["type"] == "weekly":
        if not any(keyword in text for keyword in weekly_keywords):
            return False
            
    return True

def _validate_ticket_command(params: dict, text: str) -> bool:
    """驗證淺草寺籤命令的參數"""
    if "text" not in params:
        return False
        
    # 確保原文中確實包含抽籤相關關鍵字
    keywords = command_patterns["ticket"]
    
    # 基本關鍵字匹配
    if not any(keyword in text for keyword in keywords):
        return False
        
    return True

def _validate_sixty_poem_command(params: dict, text: str) -> bool:
    """驗證六十甲子籤命令的參數"""
    if "text" not in params:
        return False
        
    # 確保原文中確實包含甲子籤相關關鍵字
    keywords = command_patterns["sixty_poem"]
    return any(keyword in text for keyword in keywords)

def _validate_lulu_chat_command(params: dict, text: str) -> bool:
    """驗證露露對話命令的參數"""
    if "text" not in params:
        return False

    # 確保原文中確實以「露露」開頭
    if not text.startswith("露露"):
        return False

    # 確保有對話內容（不只是「露露」）
    content = text[2:].strip()
    if not content:
        return False

    return True

def _validate_command_keywords(command: str, text: str) -> bool:
    """驗證命令關鍵字是否出現在原文中"""
    if command not in command_patterns:
        # 對於 lulu_chat 特殊處理
        if command == "lulu_chat":
            return text.startswith("露露")
        return False

    patterns = command_patterns[command]
    if isinstance(patterns, list):
        return any(keyword in text for keyword in patterns)
    elif isinstance(patterns, dict):
        # 對於 astro 這樣的特殊情況
        if command == "astro":
            basic_patterns = patterns.get("patterns", [])
            weekly_patterns = patterns.get("weekly_patterns", [])
            signs = patterns.get("signs", {})
            return (any(keyword in text for keyword in basic_patterns) or
                   any(keyword in text for keyword in weekly_patterns) or
                   any(sign in text for sign in signs))
    return False