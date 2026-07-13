from layout.astro_bubble import create_astro_bubble
from layout.ticket_bubble import create_ticket_bubble
from layout.podcast_bubble import create_podcast_bubble
from layout.help_bubble import create_help_bubble
from layout.answers_book_bubble import create_answers_book_bubble
from linebot.v3.messaging import FlexMessage, FlexContainer



def process_astro_bubble_reply(result: dict) -> FlexMessage:
    """
    將 use case 回傳的 normalized astro dict 轉換為 FlexMessage。

    Args:
        result: services.use_cases.astro.get_astro_result() 的回傳值
    """
    if result.get("error"):
        return FlexMessage(
            alt_text='今日運勢',
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": result["error"],
                            "weight": "bold",
                            "size": "md"
                        }
                    ]
                }
            })
        )

    # 將 fortunes list-of-dict 轉成 create_astro_bubble 需要的 [(stars, content), ...]
    star_counts = [(f["stars"], f["content"]) for f in result["fortunes"]]

    astro_bubble = create_astro_bubble(
        title=result["title"],
        star_counts=star_counts,
        reminder=result["reminder"]
    )

    flex_container = FlexContainer.from_dict(astro_bubble)
    return FlexMessage(alt_text='今日運勢', contents=flex_container)


def process_ticket_reply(result: dict) -> FlexMessage:
    """
    將 use case 回傳的 ticket dict 轉換為 FlexMessage。

    Args:
        result: services.use_cases.ticket.get_ticket_result() 的回傳值
    """
    ticket_bubble = create_ticket_bubble(
        title=result["title"],
        type=result["ticket_type"],
        poem=result["poem"],
        explain=result["explain"],
        result=result["result"],
        img_url=result["img_url"],
        ai_result=result["ai_result"],
    )
    flex_container = FlexContainer.from_dict(ticket_bubble)
    return FlexMessage(alt_text='籤詩結果', contents=flex_container)

def process_podcast_reply(result: dict) -> FlexMessage:
    """
    將 use case 回傳的 podcast dict 轉換為 FlexMessage。

    Args:
        result: services.use_cases.podcast.get_podcast_result() 的回傳值
    """
    bubble = create_podcast_bubble(result["title"], result["groups"])
    return FlexMessage(
        alt_text='本週星座運勢',
        contents=FlexContainer.from_dict(bubble)
    )

def process_help_reply(data):
    bubble = create_help_bubble(data)
    flex_message = FlexMessage(
        alt_text="使用說明",
        contents=FlexContainer.from_dict(bubble)
    )

    return flex_message


def process_answers_book_reply(result: dict) -> FlexMessage:
    """
    將 use case 回傳的 answers_book dict 轉換為 FlexMessage。

    Args:
        result: services.use_cases.answers_book.get_answers_book_result() 的回傳值
    """
    bubble = create_answers_book_bubble(result["answer"])
    return FlexMessage(alt_text='解答之書', contents=FlexContainer.from_dict(bubble))
