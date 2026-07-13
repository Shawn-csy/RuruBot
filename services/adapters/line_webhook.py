"""
LINE Webhook Adapter

負責：
- WebhookHandler 建立與事件註冊（lazy，等 get_handler() 才建立）
- handle_message：解析文字 → 呼叫 command router → 發送訊息
- callback HTTP handler（供 FastAPI 掛載）
"""
import asyncio
import os
from fastapi import Request
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from services.commands import process_message
from services.message_builder import build_messages_from_result
from services.adapters.line_sender import send_messages

LINE_TEST_REPLY_TOKEN = "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA"

_handler: WebhookHandler | None = None


def _handle_message(event: MessageEvent) -> None:
    if event.reply_token == LINE_TEST_REPLY_TOKEN:
        print("檢測到測試訊息，跳過回覆")
        return

    result = process_message(event.message.text)
    if not result:
        return

    messages = build_messages_from_result(result)
    if messages:
        send_messages(
            reply_token=event.reply_token,
            user_id=event.source.user_id,
            messages=messages,
        )


def get_handler() -> WebhookHandler:
    """Lazy init WebhookHandler，確保 load_dotenv() 已先執行。"""
    global _handler
    if _handler is None:
        _handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
        _handler.add(MessageEvent, message=TextMessageContent)(_handle_message)
    return _handler


async def callback(request: Request):
    body_bytes = await request.body()
    body = body_bytes.decode("utf-8")
    signature = request.headers.get("X-Line-Signature")

    h = get_handler()
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: h.handle(body, signature))

    return "OK"
