"""
命令處理器 - 統一的命令處理入口

負責:
1. 解析用戶輸入
2. 執行命令處理
3. 返回結果
"""
from typing import Tuple, Optional, Dict, Any
from .config import COMMAND_CONFIG


def parse_command(text: str) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    解析用戶輸入的命令

    Args:
        text: 用戶輸入文本

    Returns:
        (命令名稱, 參數字典)
    """
    if not text or not text.strip():
        return None, {}

    text = text.strip()

    # 遍歷命令配置，嘗試匹配
    for command_name, config in COMMAND_CONFIG.items():
        patterns = config["patterns"]
        exact_start = config.get("exact_start", False)

        # 檢查是否匹配模式
        matched = False
        if exact_start:
            # 必須以模式開頭
            matched = any(text.startswith(pattern) for pattern in patterns)
        else:
            # 包含模式即可
            matched = any(pattern in text for pattern in patterns)

        if matched:
            # 解析參數
            parse_func = config.get("parse")
            if parse_func:
                params = parse_func(text)
                if params is None:  # 解析失敗
                    continue
            else:
                params = {}

            print(f"✓ 匹配命令: {command_name}, 參數: {params}")
            return command_name, params

    # 如果沒有匹配，返回 None（不使用 AI 後備）
    print("✗ 未匹配到任何命令")
    return None, {}


def handle_command(command: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    處理命令

    Args:
        command: 命令名稱
        params: 命令參數

    Returns:
        回覆資料字典，格式: {"type": "...", "data": ...}
    """
    # 如果沒有命令，返回 None
    if not command:
        return None

    # 從配置表中獲取處理器
    config = COMMAND_CONFIG.get(command)
    if not config:
        print(f"✗ 未知命令: {command}")
        return None

    # 執行處理器
    try:
        handler = config["handler"]
        result = handler(params)
        return result

    except Exception as e:
        print(f"✗ 處理命令 {command} 時發生錯誤: {str(e)}")
        return {
            "type": "text",
            "data": "還沒處理完啦等我一下"
        }


def process_message(text: str) -> Optional[Dict[str, Any]]:
    """
    處理用戶訊息（一站式處理）

    Args:
        text: 用戶輸入文本

    Returns:
        回覆資料字典
    """
    command, params = parse_command(text)
    return handle_command(command, params)
