from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

MOCK_RESULT = {
    "sign": "金牛座",
    "fortune_type": "daily",
    "title": "金牛座每日運勢",
    "fortunes": [
        {"label": "整體運勢", "stars": 3, "content": "今天普通"},
        {"label": "愛情運勢", "stars": 4, "content": "感情順利"},
        {"label": "事業運勢", "stars": 3, "content": "工作穩定"},
        {"label": "財運運勢", "stars": 2, "content": "花費較多"},
    ],
    "reminder": "今天保持平常心。",
    "error": None,
}


class TestAstroAPI:

    def test_daily(self):
        with patch('api.routes.get_astro_result', return_value=MOCK_RESULT):
            resp = client.get("/api/astro", params={"sign": "金牛座", "type": "daily"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["sign"] == "金牛座"
        assert data["fortune_type"] == "daily"
        assert len(data["fortunes"]) == 4
        assert data["fortunes"][0]["label"] == "整體運勢"
        assert data["fortunes"][0]["stars"] == 3
        assert data["error"] is None

    def test_weekly(self):
        weekly_result = {**MOCK_RESULT, "fortune_type": "weekly"}
        with patch('api.routes.get_astro_result', return_value=weekly_result):
            resp = client.get("/api/astro", params={"sign": "金牛座", "type": "weekly"})
        assert resp.status_code == 200
        assert resp.json()["fortune_type"] == "weekly"

    def test_default_type_is_daily(self):
        with patch('api.routes.get_astro_result', return_value=MOCK_RESULT) as mock_uc:
            resp = client.get("/api/astro", params={"sign": "金牛座"})
        assert resp.status_code == 200
        mock_uc.assert_called_once_with("金牛座", "daily")

    def test_unknown_sign_returns_400(self):
        resp = client.get("/api/astro", params={"sign": "不存在座", "type": "daily"})
        assert resp.status_code == 400
        assert "不存在座" in resp.json()["detail"]

    def test_invalid_type_returns_400(self):
        resp = client.get("/api/astro", params={"sign": "金牛座", "type": "monthly"})
        assert resp.status_code == 400

    def test_missing_sign_returns_422(self):
        resp = client.get("/api/astro")
        assert resp.status_code == 422

    def test_upstream_error_returns_503(self):
        error_result = {**MOCK_RESULT, "error": "無法獲取星座資料"}
        with patch('api.routes.get_astro_result', return_value=error_result):
            resp = client.get("/api/astro", params={"sign": "金牛座", "type": "daily"})
        assert resp.status_code == 503

    def test_response_is_json_serializable(self):
        """確認 fortunes 是 list of dict，不是 list of tuple"""
        with patch('api.routes.get_astro_result', return_value=MOCK_RESULT):
            resp = client.get("/api/astro", params={"sign": "金牛座", "type": "daily"})
        assert resp.status_code == 200
        fortunes = resp.json()["fortunes"]
        assert isinstance(fortunes[0], dict)
        assert set(fortunes[0].keys()) == {"label", "stars", "content"}
