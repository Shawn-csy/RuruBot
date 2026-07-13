"""
每日梗圖 Use Case

負責：取得今日梗圖 URL 列表，回傳純資料，不 import LINE SDK。
"""
from datetime import datetime
from typing import Optional
import pytz
from services.features.daily_meme import get_daily_meme


def get_daily_meme_result() -> dict:
    """
    取得今日梗圖資料。

    Returns:
        {
            "date_str": "2024/01/15",
            "urls": ["https://...", ...],
            "error": None | str
        }
    """
    taipei_tz = pytz.timezone('Asia/Taipei')
    today = datetime.now(taipei_tz)
    date_str = today.strftime("%Y/%m/%d")

    urls = get_daily_meme()
    if not urls:
        return {
            "date_str": date_str,
            "urls": [],
            "error": "抱歉，今天還沒有梗圖或無法取得",
        }

    return {
        "date_str": date_str,
        "urls": urls,
        "error": None,
    }
