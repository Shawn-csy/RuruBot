def get_help_message():
    """取得幫助訊息"""
    help_content = {
        "title": "機器露露使用說明",
        "sections": [
            {
                "title": "🌧 天氣查詢",
                "commands": [
                    "雷達",
                    "radar",
                    "天氣雷達"
                ],
                "description": "查看即時氣象雷達圖"
            },
            {
                "title": "⭐ 星座運勢",
                "commands": [
                    "金牛座",
                    "-w 金牛座",
                    "想看金牛座運勢"
                ],
                "description": "查詢星座運勢（支援日運/週運）"
            },
            {
                "title": "🎋 淺草寺抽籤",
                "commands": [
                    "抽籤",
                    "淺草寺",
                    "幫我抽個籤"
                ],
                "description": "抽取淺草寺觀音籤，並提供AI解籤"
            },
            {
                "title": "🎯 六十甲子籤",
                "commands": [
                    "抽六十甲子籤",
                    "甲子籤",
                    "抽甲子籤"
                ],
                "description": "抽取傳統六十甲子籤，並提供AI解籤"
            },
            {
                "title": "📻 國師運勢",
                "commands": [
                    "國師",
                    "本週國師",
                    "唐綺陽"
                ],
                "description": "查看本週星座運勢分析"
            },
            {
                "title": "🎵 音樂推薦",
                "commands": [
                    "--m ",
                    "--ping ",
                    "--ping 人名"

                ],
                "description": "隨便推你一首歌"
            },
            {
                "title": "🔮 塔羅占卜",
                "commands": [
                    "每日塔羅：限時開放，協助測算每日運勢"
                ],
                "description": "此指令為限時開放，用完就沒惹\n"
            },

        ],
        "footer": {
            "text": "💡 小提示：你可以用自然語言跟我對話，我會理解你的意思！",
            "note": "例如：「幫我看看今天運勢」、「想問問感情運」"
        }
    }

    return help_content
