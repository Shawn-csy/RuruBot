"""
雷達回波圖 Use Case

負責：取得雷達圖 URL，回傳純資料，不 import LINE SDK。
"""
from services.features.radar import radar


def get_radar_result() -> dict:
    """
    取得最新雷達回波圖資料。

    Returns:
        {
            "urls": ["https://...", ...],
            "error": None | str
        }
    """
    urls = radar()
    if not urls:
        return {
            "urls": [],
            "error": "無法取得雷達圖，請稍後再試",
        }

    return {
        "urls": urls,
        "error": None,
    }
