import requests
import json
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# 從環境變數獲取 Channel Secret
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

# 你的 webhook URL
WEBHOOK_URL = "http://localhost:8080/callback"  # 根據你的實際設置修改

def generate_signature(body, channel_secret):
    """生成 X-Line-Signature"""
    hash = hmac.new(channel_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    return signature

def test_text_message():
    """測試發送文字訊息"""
    # 模擬 LINE 平台發送的訊息事件
    body = {
        "destination": "xxxxxxxxxx",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "12345678901234",
                    "text": "radar",
                    "quoteToken": "q123456-abcdef"
                },
                "timestamp": 1462629479859,
                "source": {
                    "type": "user",
                    "userId": "U4af4980629..."
                },
                "replyToken": "nHuyWiB7yP5Zw52FIkcQobQuGDXCTA",
                "mode": "active",
                "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                "deliveryContext": {
                    "isRedelivery": False
                }
            }
        ]
    }
    
    body_json = json.dumps(body)
    signature = generate_signature(body_json, CHANNEL_SECRET)
    
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": signature
    }
    
    print(f"發送測試訊息: {body['events'][0]['message']['text']}")
    response = requests.post(WEBHOOK_URL, headers=headers, data=body_json)
    
    print(f"回應狀態碼: {response.status_code}")
    print(f"回應內容: {response.text}")
    
    return response.status_code == 200

if __name__ == "__main__":
    print("開始測試 LINE Bot...")
    if test_text_message():
        print("測試成功！")
    else:
        print("測試失敗！") 