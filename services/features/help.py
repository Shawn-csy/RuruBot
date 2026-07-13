def get_help_message():
    """取得幫助訊息"""
    help_content = {
        "title": "RuruBot 使用說明",
        "sections": [
            {
                "title": "🌧 氣象雷達",
                "commands": [
                    "雷達",
                    "radar"
                ],
                "description": "查看即時氣象雷達圖"
            },
            {
                "title": "⭐ 星座運勢",
                "commands": [
                    "牡羊座",
                    "-w 牡羊座"
                ],
                "description": "日運：直接輸入星座名　週運：-w 星座名"
            },
            {
                "title": "🎋 淺草寺抽籤",
                "commands": [
                    "抽淺草寺",
                    "抽淺草寺 工作運"
                ],
                "description": "抽淺草寺觀音籤，可加上問題獲得 AI 解籤"
            },
            {
                "title": "📻 本週國師",
                "commands": [
                    "本週國師"
                ],
                "description": "查看本週唐綺陽星座運勢速報"
            },
            {
                "title": "🐶 暈船迷因",
                "commands": [
                    "暈船仔",
                    "暈船"
                ],
                "description": "隨機取得暈船迷因圖"
            },
            {
                "title": "📖 解答之書",
                "commands": [
                    "解答之書 我會成功嗎"
                ],
                "description": "向解答之書提問，得到一個答案"
            },
        ],
        "footer": {
            "text": "輸入 --help 隨時查看此說明",
            "note": "啊你都已經打開這個了，應該沒問題了吧(?)"
        }
    }

    return help_content
