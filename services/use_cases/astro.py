"""
星座 use case

不 import LINE SDK。
回傳純資料 dict，可被 LINE presenter 或 REST API 共用。
"""
import re
from typing import List
from services.features.astro import get_astro_info

FORTUNE_TYPES = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]


def _parse_title(content_lines: List[str]) -> str:
    for line in content_lines:
        if "解析" in line or "運勢" in line:
            return line.strip()
    if len(content_lines) > 1:
        return content_lines[1].strip()
    return "今日運勢"


def _parse_fortunes(content_lines: List[str]) -> List[dict]:
    """回傳 [{"label": str, "stars": int, "content": str}, ...] 對應 FORTUNE_TYPES 順序"""
    results = []
    for fortune_type in FORTUNE_TYPES:
        found = False
        for line in content_lines:
            if fortune_type in line:
                match = re.search(r'(.*?)：(.*)', line)
                if match:
                    stars = match.group(1).count('★')
                    content = match.group(2).strip()
                    results.append({"label": fortune_type, "stars": stars, "content": content})
                    found = True
                    break
        if not found:
            results.append({"label": fortune_type, "stars": 0, "content": "暫無資料"})
    return results


def _parse_reminder(data: List[str], content_lines: List[str]) -> str:
    if len(data) > 1 and data[1].strip():
        return data[1].strip()
    if content_lines and not any(ft in content_lines[-1] for ft in FORTUNE_TYPES):
        return content_lines[-1].strip()
    return "今天也要加油喔！"


def get_astro_result(sign: str, fortune_type: str) -> dict:
    """
    取得並 normalize 星座運勢資料。

    Args:
        sign: 星座名（如 "金牛座"）
        fortune_type: "daily" 或 "weekly"

    Returns:
        {
            "sign": str,
            "fortune_type": str,
            "title": str,
            "fortunes": [{"label": str, "stars": int, "content": str}, ...],
            "reminder": str,
            "error": str | None
        }
    """
    raw = get_astro_info(sign, fortune_type)

    if not raw or not isinstance(raw, list):
        return {
            "sign": sign,
            "fortune_type": fortune_type,
            "title": "今日運勢",
            "fortunes": [{"label": ft, "stars": 0, "content": "暫無資料"} for ft in FORTUNE_TYPES],
            "reminder": "無法獲取星座資料",
            "error": "無法獲取星座資料",
        }

    content_lines = raw[0].strip().split('\n')
    return {
        "sign": sign,
        "fortune_type": fortune_type,
        "title": _parse_title(content_lines),
        "fortunes": _parse_fortunes(content_lines),
        "reminder": _parse_reminder(raw, content_lines),
        "error": None,
    }
