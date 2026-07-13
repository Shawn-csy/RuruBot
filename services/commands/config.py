"""
命令配置表

集中管理所有命令的匹配模式、解析器和處理器
"""
from services.constants import astro as astro_dict
from .parsers import (
    parse_astro_params,
    parse_astro_weekly_flag_params,
    parse_ticket_params,
    parse_answers_book_params,
)
from .handlers import (
    handle_radar,
    handle_astro,
    handle_ticket,
    handle_podcast,
    handle_help,
    handle_dogmeme,
    handle_answers_book,
)


# 命令配置表
# 格式:
# "命令名": {
#     "patterns": [匹配模式列表],
#     "parse": 參數解析函數（可選）,
#     "handler": 處理函數,
#     "exact_start": 是否必須以模式開頭（可選）
# }

COMMAND_CONFIG = {
    "radar": {
        "patterns": ["雷達", "radar"],
        "parse": None,
        "handler": handle_radar,
        "exact_start": True,
        "description": "顯示氣象雷達圖"
    },

    "astro": {
        "patterns": list(astro_dict.keys()),
        "parse": parse_astro_params,
        "handler": handle_astro,
        "exact_start": True,
        "description": "查詢星座運勢"
    },

    "astro_weekly": {
        "patterns": ["-w"],
        "parse": parse_astro_weekly_flag_params,
        "handler": handle_astro,
        "exact_start": True,
        "description": "查詢星座每週運勢（-w 星座名）"
    },

    "ticket": {
        "patterns": ["抽淺草寺"],
        "parse": parse_ticket_params,
        "handler": handle_ticket,
        "exact_start": True,
        "description": "抽淺草寺籤"
    },

    "podcast": {
        "patterns": ["本週國師"],
        "parse": None,
        "handler": handle_podcast,
        "exact_start": True,
        "description": "本週國師運勢"
    },

    "help": {
        "patterns": ["--help"],
        "parse": None,
        "handler": handle_help,
        "exact_start": True,
        "description": "使用說明"
    },

    "dogmeme": {
        "patterns": ["暈船仔", "暈船"],
        "parse": None,
        "handler": handle_dogmeme,
        "exact_start": True,
        "description": "暈船迷因圖"
    },

    "answers_book": {
        "patterns": ["解答之書"],
        "parse": parse_answers_book_params,
        "handler": handle_answers_book,
        "exact_start": True,
        "description": "解答之書（隨機抽一條答案）"
    },

}


def get_command_list():
    """獲取所有命令列表（用於幫助文檔）"""
    return [
        {
            "name": name,
            "description": config.get("description", ""),
            "patterns": config["patterns"]
        }
        for name, config in COMMAND_CONFIG.items()
    ]
