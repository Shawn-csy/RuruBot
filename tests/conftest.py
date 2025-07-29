import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from linebot.v3.messaging import (
    Configuration,
    TextMessage,
    ImageMessage,
    FlexMessage,
    FlexContainer
)

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_gemini_response():
    """模擬 Gemini API 回應"""
    return {
        "command": "ticket",
        "params": {
            "text": "工作運"
        }
    }

@pytest.fixture(autouse=True)
def mock_gemini_api():
    """自動 mock Gemini API 回應"""
    with patch('services.features.gemini_reply.get_gemini_reply') as mock:
        def mock_response(prompt):
            # 根據提示詞內容返回不同的回應
            if any(word in prompt for word in ["運勢", "星座"]):
                return '{"command": "astro", "params": {"astro_name": "金牛座", "type": "daily"}}'
            elif any(word in prompt for word in ["抽籤", "抽個籤", "淺草寺"]):
                return '{"command": "ticket", "params": {"text": "一般運勢"}}'
            elif "雷達" in prompt:
                return '{"command": "radar", "params": {}}'
            elif "國師" in prompt:
                return '{"command": "podcast", "params": {}}'
            else:
                return None
        mock.side_effect = mock_response
        yield mock

@pytest.fixture
def mock_line_bot_api():
    """Mock Line Bot API"""
    mock_api = MagicMock()
    mock_api.reply_message = MagicMock()
    return mock_api

@pytest.fixture
def mock_api_client():
    """Mock API Client"""
    with patch('linebot.v3.messaging.ApiClient') as mock:
        yield mock

@pytest.fixture
def mock_messaging_api():
    """Mock Messaging API"""
    with patch('linebot.v3.messaging.MessagingApi') as mock:
        yield mock

@pytest.fixture
def mock_flex_container():
    """Mock Flex Container"""
    return FlexContainer.from_dict({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": []
        }
    }) 