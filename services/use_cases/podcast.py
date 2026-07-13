"""
國師運勢 Use Case

負責：從 Spotify 取得 podcast，解析成結構化資料，不 import LINE SDK。
"""
from services.features.get_podcast import get_podcast


def _parse_podcast_string(text: str) -> dict:
    """
    將 get_podcast() 回傳的格式化字串解析成結構化 dict。

    輸入格式範例：
        【本週運勢】2024/1/1
        【讚的】
        牡羊：本週極佳
        【累的】
        金牛：需要休息

    Returns:
        {
            "title": "【本週運勢】...",
            "groups": {
                "累的": [{"sign": "牡羊", "fortune": "..."}],
                "穩的": [...],
                "讚的": [...]
            }
        }
    """
    lines = text.strip().split('\n')

    title_lines = []
    weekly_title_prefixes = ("【本週提醒】", "【本週運勢】", "【本周提醒】", "【本周運勢】")
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith(weekly_title_prefixes):
            title_lines.append(line)
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith("【"):
                title_lines.append(lines[j].strip())
                j += 1
            break
    title = " ".join(title_lines) if title_lines else (lines[0].strip() if lines else "【本週運勢】")

    groups = {"累的": [], "穩的": [], "讚的": []}
    current_group = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "【" in line and "】" in line:
            for g in groups:
                if g in line:
                    current_group = g
                    break
            continue
        if current_group and "：" in line:
            sign, _, fortune = line.partition("：")
            if sign.strip():
                groups[current_group].append({"sign": sign.strip(), "fortune": fortune.strip()})

    return {"title": title, "groups": groups}


def get_podcast_result() -> dict:
    """
    取得本週國師運勢結構化資料。

    Returns:
        {
            "title": "【本週運勢】...",
            "groups": {
                "累的": [{"sign": "牡羊", "fortune": "..."}, ...],
                "穩的": [...],
                "讚的": [...]
            },
            "error": None | str
        }
    """
    raw = get_podcast()

    # get_podcast() 在失敗時回傳錯誤字串（不含【】分類格式）
    if not raw or not any(tag in raw for tag in ("【讚的】", "【累的】", "【穩的】")):
        return {
            "title": "",
            "groups": {"累的": [], "穩的": [], "讚的": []},
            "error": raw or "無法取得本週國師運勢",
        }

    parsed = _parse_podcast_string(raw)
    return {
        "title": parsed["title"],
        "groups": parsed["groups"],
        "error": None,
    }
