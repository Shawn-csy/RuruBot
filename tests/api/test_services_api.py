from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_radar_api_success():
    result = {"urls": ["https://example.com/radar.png"], "error": None}
    with patch("api.routes.get_radar_result", return_value=result):
        resp = client.get("/api/radar")
    assert resp.status_code == 200
    assert resp.json() == result


def test_radar_api_error_returns_503():
    with patch("api.routes.get_radar_result", return_value={"urls": [], "error": "無法取得雷達圖"}):
        resp = client.get("/api/radar")
    assert resp.status_code == 503


def test_ticket_api_disables_ai():
    result = {
        "title": "第001籤",
        "ticket_type": "大吉",
        "poem": "春色滿園",
        "explain": "萬事如意",
        "result": "順利",
        "img_url": "https://example.com/001.jpg",
        "ai_result": "",
        "error": None,
    }
    with patch("api.routes.get_ticket_result", return_value=result) as mock_uc:
        resp = client.post("/api/ticket", json={"question": "我該換工作嗎"})
    assert resp.status_code == 200
    assert resp.json()["ai_result"] == ""
    mock_uc.assert_called_once_with("我該換工作嗎", with_ai=False)


def test_ticket_api_ignores_with_ai_payload():
    result = {
        "title": "第001籤",
        "ticket_type": "大吉",
        "poem": "春色滿園",
        "explain": "萬事如意",
        "result": "順利",
        "img_url": "https://example.com/001.jpg",
        "ai_result": "",
        "error": None,
    }
    with patch("api.routes.get_ticket_result", return_value=result) as mock_uc:
        resp = client.post("/api/ticket", json={"question": "我該換工作嗎", "with_ai": True})
    assert resp.status_code == 200
    assert resp.json()["ai_result"] == ""
    mock_uc.assert_called_once_with("我該換工作嗎", with_ai=False)


def test_ticket_api_error_returns_503():
    with patch("api.routes.get_ticket_result", return_value={"error": "籤詩服務暫時無法使用"}):
        resp = client.post("/api/ticket", json={"question": ""})
    assert resp.status_code == 503


def test_podcast_api_success():
    result = {
        "title": "【本週運勢】",
        "groups": {"累的": [], "穩的": [], "讚的": [{"sign": "牡羊", "fortune": "很好"}]},
        "error": None,
    }
    with patch("api.routes.get_podcast_result", return_value=result):
        resp = client.get("/api/podcast")
    assert resp.status_code == 200
    assert resp.json() == result


def test_podcast_api_error_returns_503():
    with patch("api.routes.get_podcast_result", return_value={"title": "", "groups": {}, "error": "尚未更新"}):
        resp = client.get("/api/podcast")
    assert resp.status_code == 503


def test_answers_book_api_success():
    result = {"question": "我會成功嗎", "answer": "是的", "error": None}
    with patch("api.routes.get_answers_book_result", return_value=result) as mock_uc:
        resp = client.post("/api/answers-book", json={"question": "我會成功嗎"})
    assert resp.status_code == 200
    assert resp.json() == result
    mock_uc.assert_called_once_with("我會成功嗎")


def test_answers_book_api_error_returns_503():
    with patch("api.routes.get_answers_book_result", return_value={"question": "", "answer": "", "error": "無法使用"}):
        resp = client.post("/api/answers-book", json={})
    assert resp.status_code == 503


def test_help_api_success():
    result = {"title": "使用說明", "sections": [], "footer": {"text": "", "note": ""}}
    with patch("api.routes.get_help_message", return_value=result):
        resp = client.get("/api/help")
    assert resp.status_code == 200
    assert resp.json() == result


def test_cors_preflight_allows_frontend_origin():
    resp = client.options(
        "/api/radar",
        headers={
            "Origin": "https://example-frontend.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == "*"
