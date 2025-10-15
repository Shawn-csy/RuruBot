def create_tarot_help_bubble():
    """建立塔羅占卜詳細說明的 Bubble"""
    bubble = {
        "type": "bubble",
        "size": "giga",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🔮 塔羅占卜使用說明",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#ffffff",
                    "align": "center"
                }
            ],
            "backgroundColor": "#6B4A8E",
            "paddingAll": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 基本使用方式區塊
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📋 基本使用方式",
                            "weight": "bold",
                            "size": "md",
                            "color": "#6B4A8E"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "▸ 基本指令：-塔羅",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": "（使用預設牌陣「時間之流」，問題為「今天的運勢如何？」）",
                                    "size": "xxs",
                                    "color": "#aaaaaa",
                                    "wrap": True,
                                    "margin": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": "▸ 帶問題：-塔羅 我的感情運勢如何？",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "（使用預設牌陣，自訂問題）",
                                    "size": "xxs",
                                    "color": "#aaaaaa",
                                    "wrap": True,
                                    "margin": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": "▸ 指定牌陣：-塔羅 二擇一 要A還是B？",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "（指定牌陣名稱 + 自訂問題）",
                                    "size": "xxs",
                                    "color": "#aaaaaa",
                                    "wrap": True,
                                    "margin": "xs"
                                }
                            ],
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#f8f5ff",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm"
                },

                # 支援的牌陣區塊
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎴 支援的牌陣",
                            "weight": "bold",
                            "size": "md",
                            "color": "#6B4A8E"
                        },
                        # 初階牌陣
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "【初階牌陣 - 3張牌】",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#444444"
                                },
                                {
                                    "type": "text",
                                    "text": "• 時間之流（預設）\n  過去→現在→未來\n  適合：日常運勢、整體趨勢",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                },
                                {
                                    "type": "text",
                                    "text": "• 問題解決\n  原因→現況→對策\n  適合：解決具體問題",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ],
                            "margin": "sm"
                        },
                        # 進階牌陣
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "【進階牌陣 - 4-7張牌】",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#444444",
                                    "margin": "md"
                                },
                                {
                                    "type": "text",
                                    "text": "• 四要素 | 二擇一 | 馬蹄鐵 | 靈感對應\n  適合：深入分析、重要決策",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        },
                        # 高階牌陣
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "【高階牌陣 - 9-10張牌】",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#444444",
                                    "margin": "md"
                                },
                                {
                                    "type": "text",
                                    "text": "• 塞爾特 | 三擇一\n  適合：全面深度分析",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "sm"
                                }
                            ]
                        }
                    ],
                    "backgroundColor": "#f8f5ff",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm"
                },

                # 使用建議區塊
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💡 使用建議",
                            "weight": "bold",
                            "size": "md",
                            "color": "#6B4A8E"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "1. 問題要具體明確\n   ✅ 好：「我這份工作該繼續還是轉職？」\n   ❌ 差：「我的未來怎麼樣？」",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": "2. 選擇合適的牌陣\n   • 日常問題 → 時間之流（3張）\n   • 具體困擾 → 問題解決（3張）\n   • 二選一 → 二擇一（5張）\n   • 深度分析 → 塞爾特（10張）",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "md"
                                },
                                {
                                    "type": "text",
                                    "text": "3. 保持開放的心態\n   塔羅是指引工具，不是絕對預言",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "md"
                                },
                                {
                                    "type": "text",
                                    "text": "4. 同一問題不建議短時間內重複占卜\n   建議至少間隔一週以上",
                                    "size": "xs",
                                    "color": "#666666",
                                    "wrap": True,
                                    "margin": "md"
                                }
                            ],
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#f8f5ff",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm"
                },

                # 範例指令區塊
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 範例指令",
                            "weight": "bold",
                            "size": "md",
                            "color": "#6B4A8E"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "-塔羅",
                                    "size": "xs",
                                    "color": "#666666"
                                },
                                {
                                    "type": "text",
                                    "text": "-塔羅 我最近的感情運勢如何？",
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": "-塔羅 問題解決 如何改善人際關係？",
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": "-塔羅 二擇一 接受新工作還是留下？",
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": "-塔羅 塞爾特 關於我的人生方向",
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "xs"
                                }
                            ],
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#f8f5ff",
                    "cornerRadius": "md",
                    "paddingAll": "md",
                    "margin": "sm"
                }
            ],
            "spacing": "sm",
            "paddingAll": "md"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "💫 祝你占卜順利！",
                    "wrap": True,
                    "color": "#ffffff",
                    "size": "sm",
                    "align": "center"
                }
            ],
            "backgroundColor": "#6B4A8E",
            "paddingAll": "md"
        }
    }

    return bubble
