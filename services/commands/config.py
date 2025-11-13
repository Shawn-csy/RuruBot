"""
命令配置表

集中管理所有命令的匹配模式、解析器和處理器
"""
from services.constants import astro as astro_dict
from .parsers import (
    parse_astro_params,
    parse_ticket_params,
    parse_sixty_poem_params,
    parse_music_params,
    parse_lulu_chat_params,
    parse_tarot_params
)
from .handlers import (
    handle_radar,
    handle_astro,
    handle_ticket,
    handle_sixty_poem,
    handle_podcast,
    handle_music,
    handle_help,
    handle_lulu_chat,
    handle_tarot,
    handle_dogmeme
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

    "ticket": {
        "patterns": ["抽淺草寺"],
        "parse": parse_ticket_params,
        "handler": handle_ticket,
        "exact_start": True,
        "description": "抽淺草寺籤"
    },

    "sixty_poem": {
        "patterns": ["抽六十甲子籤"],
        "parse": parse_sixty_poem_params,
        "handler": handle_sixty_poem,
        "exact_start": True,
        "description": "抽六十甲子籤"
    },

    "podcast": {
        "patterns": ["本週國師"],
        "parse": None,
        "handler": handle_podcast,
        "exact_start": True,
        "description": "本週國師運勢"
    },

    "music": {
        "patterns": ["--m", "--ping"],
        "parse": parse_music_params,
        "handler": handle_music,
        "exact_start": True,
        "description": "音樂推薦"
    },

    "help": {
        "patterns": ["--help"],
        "parse": None,
        "handler": handle_help,
        "exact_start": True,
        "description": "使用說明"
    },

    "lulu_chat": {
        "patterns": ["露露"],
        "parse": parse_lulu_chat_params,
        "handler": handle_lulu_chat,
        "exact_start": True,
        "description": "與露露對話"
    },

    "tarot": {
        "patterns": ["每日塔羅", "本日塔羅", "-塔羅"],
        "parse": parse_tarot_params,
        "handler": handle_tarot,
        "exact_start": True,
        "description": "塔羅占卜"
    },

    "dogmeme": {
        "patterns": ["暈船仔", "暈船"],
        "parse": None,
        "handler": handle_dogmeme,
        "exact_start": True,
        "description": "暈船迷因圖"
    }
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
