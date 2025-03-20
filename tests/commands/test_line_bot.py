import json
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app, handler
from unittest.mock import patch
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    Source,
)

load_dotenv()
client = TestClient(app)

@patch('linebot.v3.WebhookHandler.handle')
def test_text_message(mock_handle):
    """測試文字訊息處理"""
    request_body = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "測試訊息",
                "id": "test-message-id"
            },
            "timestamp": 1462629479859,
            "source": {
                "type": "user",
                "userId": "test-user-id"
            },
            "replyToken": "test-reply-token",
            "mode": "active",
            "webhookEventId": "test-webhook-id",
            "deliveryContext": {
                "isRedelivery": False
            }
        }]
    }
    
    # 生成有效的簽名
    body_json = json.dumps(request_body)
    channel_secret = os.getenv("CHANNEL_SECRET", "test-channel-secret")
    hash = hmac.new(
        channel_secret.encode('utf-8'),
        body_json.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    
    response = client.post(
        "/callback",
        headers={"X-Line-Signature": signature},
        json=request_body
    )
    
    assert response.status_code == 200
    mock_handle.assert_called_once()

def test_root():
    """測試根路徑"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

@patch('main.handler.handle')
def test_webhook_handler(mock_handle):
    """測試 webhook 處理器"""
    event = MessageEvent.parse_obj({
        "type": "message",
        "message": {
            "type": "text",
            "text": "測試訊息",
            "id": "test-message-id"
        },
        "timestamp": 1462629479859,
        "source": {
            "type": "user",
            "userId": "test-user-id"
        },
        "replyToken": "test-reply-token",
        "mode": "active",
        "webhookEventId": "test-webhook-id",
        "deliveryContext": {
            "isRedelivery": False
        }
    })
    
    handler.handle(json.dumps({
        "events": [event.dict()]
    }), "test-signature")
    
    mock_handle.assert_called_once() 