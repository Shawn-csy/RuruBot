"""
AI 命令解析器 - 簡化版
"""
from services.features.gemini_reply import get_gemini_reply
from services.commands.config import COMMAND_CONFIG
import json
import re


def parse_command_with_ai(text: str) -> tuple:
    """
    使用 AI 解析用戶指令

    Args:
        text: 用戶輸入文本

    Returns:
        (command_name, params) 或 (None, {})
    """
    try:
        # 構建 AI 提示詞
        prompt = _build_ai_prompt(text)

        # 獲取 AI 回應
        response = get_gemini_reply(prompt)

        # 提取 JSON
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if not json_match:
            return None, {}

        # 解析 JSON
        result = json.loads(json_match.group())

        # 簡單驗證
        if not isinstance(result, dict):
            return None, {}

        command = result.get("command")
        params = result.get("params", {})

        # AI 無法識別或命令不存在
        if not command or command == "null":
            return None, {}

        # 檢查命令是否在配置中
        if command not in COMMAND_CONFIG:
            return None, {}

        return command, params

    except Exception as e:
        print(f"AI 解析錯誤: {str(e)}")
        return None, {}


def _build_ai_prompt(text: str) -> str:
    """構建 AI 提示詞"""
    # 從配置中獲取所有命令名稱
    commands = list(COMMAND_CONFIG.keys())

    prompt = f"""你是一個智能指令解析器。請將用戶輸入解析為命令。

可用命令: {', '.join(commands)}

規則:
1. 返回 JSON 格式: {{"command": "命令名", "params": {{參數}}}}
2. 如果無法識別，返回: {{"command": null, "params": {{}}}}
3. 只返回 JSON，不要其他文字

用戶輸入: {text}
"""
    return prompt
