def create_answers_book_bubble(answer: str) -> dict:
    return {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#2C2C54",
            "paddingAll": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "解答之書",
                    "weight": "bold",
                    "size": "md",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "xl",
            "justifyContent": "center",
            "contents": [
                {
                    "type": "text",
                    "text": answer,
                    "size": "xl",
                    "weight": "bold",
                    "wrap": True,
                    "align": "center",
                    "color": "#2C2C54"
                }
            ]
        }
    }
