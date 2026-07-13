"""
LINE 訊息發送器

負責：
- 持有 LINE Bot API client
- reply/push 分批邏輯（Reply API 最多 5 則限制）
"""
import os
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, PushMessageRequest
)

LINE_REPLY_LIMIT = 5


_line_bot_api: MessagingApi | None = None


def _get_line_bot_api() -> MessagingApi:
    global _line_bot_api
    if _line_bot_api is None:
        configuration = Configuration(access_token=os.getenv("CHANNEL_ACCESS_TOKEN"))
        _line_bot_api = MessagingApi(ApiClient(configuration))
    return _line_bot_api


def send_messages(reply_token: str, user_id: str, messages: list) -> None:
    """
    發送訊息給使用者。

    Reply API 最多 5 則；超過時先 reply 前 5 則，
    剩下的用 push 每批 5 則分送。

    Args:
        reply_token: LINE reply token
        user_id: LINE user ID（超過 5 則時用於 push）
        messages: LINE message 物件列表
    """
    if not messages:
        return

    api = _get_line_bot_api()

    if len(messages) <= LINE_REPLY_LIMIT:
        api.reply_message(
            ReplyMessageRequest(reply_token=reply_token, messages=messages)
        )
    else:
        api.reply_message(
            ReplyMessageRequest(reply_token=reply_token, messages=messages[:LINE_REPLY_LIMIT])
        )
        remaining = messages[LINE_REPLY_LIMIT:]
        for i in range(0, len(remaining), LINE_REPLY_LIMIT):
            api.push_message(
                PushMessageRequest(to=user_id, messages=remaining[i:i + LINE_REPLY_LIMIT])
            )
