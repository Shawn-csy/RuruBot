"""
系統常量配置
"""

# 星座映射
astro = {
    '牡羊座': 0,
    '金牛座': 1,
    '雙子座': 2,
    '巨蟹座': 3,
    '獅子座': 4,
    '處女座': 5,
    '天秤座': 6,
    '天蠍座': 7,
    '射手座': 8,
    '魔羯座': 9,
    '水瓶座': 10,
    '雙魚座': 11
}

# 星座圖標
astro_icons = {
    "牡羊座": "♈",
    "金牛座": "♉",
    "雙子座": "♊",
    "巨蟹座": "♋",
    "獅子座": "♌",
    "處女座": "♍",
    "天秤座": "♎",
    "天蠍座": "♏",
    "射手座": "♐",
    "魔羯座": "♑",
    "水瓶座": "♒",
    "雙魚座": "♓"
}

# 星座運勢類型
astro_type = ['today', 'weekly', 'monthly']

# Gemini AI 系統提示詞（籤詩解讀用）
gemini_system_prompt = "你是一個專門解籤的黑貓仙人,名稱是露露，擅長根據收到的問題,理解出意思後，再依照籤詩結果，給出簡短的解釋和建議，通常不超過30字。"

# 露露對話人設
lulu_chat_system_prompt = """你是露露，一隻黑貓，

個性特點：
- 有一點賤賤的貓

回覆風格：
- 保持對話自然流暢
- 回覆長度簡短，通常只回覆喵，不說話

請用這個人設和用戶進行對話。"""

# Spotify 用戶映射表
playlist_provider = {
    "鼠藥": "https://open.spotify.com/user/nightshu?si=afef7ca34d8048da",
    "兔子": "https://open.spotify.com/user/suminxin?si=f76719fcd25a4160",
    "ㄉㄉ": "https://open.spotify.com/user/31nawtug7zzoostbgkvvtbufeplm?si=c142cf13057940f8"
}

# 播放清單（預留）
playlist = []
