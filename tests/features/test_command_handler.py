from unittest.mock import patch
from services.commands import handle_command
from services.results import VALID_RESULT_TYPES
from linebot.v3.messaging import FlexMessage


def assert_valid_result(result):
    """
    驗證 handler 回傳符合契約：
    - None（合法 no-reply）
    - {"type": VALID_RESULT_TYPES, "data": Any}
    """
    if result is None:
        return
    assert isinstance(result, dict), f"期望 dict 或 None，得到 {type(result)}"
    assert "type" in result, "缺少 'type' key"
    assert "data" in result, "缺少 'data' key"
    assert result["type"] in VALID_RESULT_TYPES, f"type={result['type']!r} 不在 VALID_RESULT_TYPES"


# ── mock data fixtures ────────────────────────────────────────────────────────

MOCK_ASTRO_RESULT = {
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

MOCK_TICKET_RESULT = {
    "title": "第001籤",
    "ticket_type": "大吉",
    "poem": "春色滿園關不住",
    "explain": "萬事如意",
    "result": "順利",
    "img_url": "https://example.com/ticket.jpg",
    "ai_result": "解籤結果",
    "error": None,
}

MOCK_HELP_DATA = {
    "title": "使用說明",
    "sections": [{"title": "測試", "commands": ["cmd"], "description": "desc"}],
    "footer": {"text": "tip", "note": "example"}
}


# ── Phase 1: 格式契約測試 ─────────────────────────────────────────────────────

class TestCommandHandlerResultFormat:
    """所有 handler 回傳必須符合 {type, data} 契約或 None"""

    def test_handle_astro_daily(self):
        with patch('services.commands.handlers.get_astro_result', return_value=MOCK_ASTRO_RESULT):
            result = handle_command("astro", {"astro_name": "金牛座", "type": "daily"})
        assert_valid_result(result)
        assert result["type"] == "flex"

    def test_handle_astro_weekly(self):
        with patch('services.commands.handlers.get_astro_result', return_value=MOCK_ASTRO_RESULT):
            result = handle_command("astro", {"astro_name": "金牛座", "type": "weekly"})
        assert_valid_result(result)
        assert result["type"] == "flex"

    def test_handle_astro_invalid_sign(self):
        result = handle_command("astro", {"astro_name": "不存在座", "type": "daily"})
        assert_valid_result(result)
        assert result["type"] == "text"

    def test_handle_radar(self):
        with patch('services.commands.handlers.get_radar_result', return_value={"urls": ["https://example.com/radar.jpg"], "error": None}):
            result = handle_command("radar", {})
        assert_valid_result(result)
        assert result["type"] == "mixed"

    def test_handle_radar_empty_returns_none(self):
        """radar 無結果回 None（合法 no-reply）"""
        with patch('services.commands.handlers.get_radar_result', return_value={"urls": [], "error": "無法取得"}):
            result = handle_command("radar", {})
        assert result is None

    def test_handle_ticket(self):
        with patch('services.commands.handlers.get_ticket_result', return_value=MOCK_TICKET_RESULT):
            result = handle_command("ticket", {"text": "工作運"})
        assert_valid_result(result)
        assert result["type"] == "flex"

    def test_handle_podcast(self):
        mock_result = {
            "title": "【本週運勢】",
            "groups": {"讚的": [{"sign": "牡羊", "fortune": "本週極佳"}], "穩的": [], "累的": []},
            "error": None,
        }
        with patch('services.commands.handlers.get_podcast_result', return_value=mock_result):
            result = handle_command("podcast", {})
        assert_valid_result(result)
        assert result["type"] == "flex"

    def test_handle_help(self):
        with patch('services.commands.handlers.get_help_message', return_value=MOCK_HELP_DATA):
            result = handle_command("help", {})
        assert_valid_result(result)
        assert result["type"] == "flex"

    def test_handle_dogmeme(self):
        with patch('services.commands.handlers.dogdog_meme', return_value="https://example.com/meme.jpg"):
            result = handle_command("dogmeme", {})
        assert_valid_result(result)
        assert result["type"] == "mixed"

    def test_handle_answers_book(self):
        mock_result = {"question": "我會成功嗎", "answer": "是的", "error": None}
        with patch('services.commands.handlers.get_answers_book_result', return_value=mock_result):
            result = handle_command("answers_book", {"question": "我會成功嗎"})
        assert_valid_result(result)
        assert result["type"] == "flex"

    def test_handle_none_command(self):
        result = handle_command(None, {})
        assert result is None

    def test_handle_unknown_command(self):
        result = handle_command("nonexistent", {})
        assert result is None

    def test_handle_exception_fallback(self):
        """handler 拋例外時，processor 回傳標準 error dict"""
        with patch('services.commands.handlers.get_astro_result', side_effect=Exception("爆了")):
            result = handle_command("astro", {"astro_name": "金牛座", "type": "daily"})
        assert_valid_result(result)
        assert result["type"] == "text"


# ── 基本功能測試（保留原有）────────────────────────────────────────────────────

class TestCommandHandler:

    def test_handle_astro(self):
        with patch('services.commands.handlers.get_astro_result', return_value=MOCK_ASTRO_RESULT):
            result = handle_command("astro", {"astro_name": "金牛座", "type": "daily"})
        assert result["type"] == "flex"
        assert isinstance(result["data"], FlexMessage)

    def test_handle_ticket(self):
        with patch('services.commands.handlers.get_ticket_result', return_value=MOCK_TICKET_RESULT):
            result = handle_command("ticket", {"text": "工作運"})
        assert result["type"] == "flex"
        assert isinstance(result["data"], FlexMessage)

    def test_handle_radar(self):
        with patch('services.commands.handlers.get_radar_result', return_value={"urls": ["https://example.com/radar.jpg"], "error": None}):
            result = handle_command("radar", {})
        assert result["type"] == "mixed"
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0

    def test_handle_invalid(self):
        assert handle_command(None, {}) is None
