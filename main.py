import sys
import os

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
import uvicorn
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

import os
from services.commands import process_message
from services.message_builder import build_messages_from_result
 
#測試使用 正式版移除
import sys
sys.stdout.flush()

load_dotenv()

app = FastAPI()
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
configuration = Configuration(access_token=os.getenv("CHANNEL_ACCESS_TOKEN"))

# 初始化 LINE Bot API（全局單例）
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/callback")
async def callback(request: Request):
    body_bytes = await request.body()
    body = body_bytes.decode('utf-8')
    signature = request.headers.get("X-Line-Signature")
    handler.handle(body, signature)
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 測試訊息
    if event.reply_token == "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA":
        print("檢測到測試訊息，跳過回覆")
        return

    # 處理訊息（解析 + 處理）
    result = process_message(event.message.text)

    # 構建並發送訊息
    if result:
        messages = build_messages_from_result(result)
        if messages:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)