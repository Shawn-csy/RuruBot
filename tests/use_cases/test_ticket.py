"""
tests/use_cases/test_ticket.py

測試淺草寺抽籤 use case，不打真實外部 API。
"""
import ast
from unittest.mock import patch
from services.use_cases.ticket import get_ticket_result

MOCK_TICKET_DATA = (
    ["第001籤", "大吉", "春色滿園", "萬事如意", "順利"],
    "https://storage.googleapis.com/linebot01/img/001.jpg"
)


def test_no_line_sdk_import():
    """use case 不能 import LINE SDK"""
    import services.use_cases.ticket as mod
    source = open(mod.__file__).read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                assert "linebot" not in (name or ""), f"LINE SDK imported: {name}"


def test_returns_ticket_data_no_question():
    with patch("services.use_cases.ticket.locat_ticket", return_value=MOCK_TICKET_DATA):
        result = get_ticket_result("")
    assert result["error"] is None
    assert result["title"] == "第001籤"
    assert result["ticket_type"] == "大吉"
    assert result["ai_result"] == "喵？"


def test_calls_gemini_when_question():
    with patch("services.use_cases.ticket.locat_ticket", return_value=MOCK_TICKET_DATA), \
         patch("services.use_cases.ticket.get_gemini_reply", return_value="解籤結果") as mock_gemini:
        result = get_ticket_result("感情運如何")
    assert result["ai_result"] == "解籤結果"
    mock_gemini.assert_called_once()
    call_arg = mock_gemini.call_args[0][0]
    assert "感情運如何" in call_arg


def test_skips_gemini_when_with_ai_false():
    with patch("services.use_cases.ticket.locat_ticket", return_value=MOCK_TICKET_DATA), \
         patch("services.use_cases.ticket.get_gemini_reply") as mock_gemini:
        result = get_ticket_result("感情運如何", with_ai=False)
    assert result["ai_result"] == ""
    mock_gemini.assert_not_called()


def test_returns_all_required_keys():
    with patch("services.use_cases.ticket.locat_ticket", return_value=MOCK_TICKET_DATA):
        result = get_ticket_result("")
    for key in ("title", "ticket_type", "poem", "explain", "result", "img_url", "ai_result", "error"):
        assert key in result, f"missing key: {key}"


def test_error_on_exception():
    with patch("services.use_cases.ticket.locat_ticket", side_effect=Exception("爆了")):
        result = get_ticket_result("")
    assert result["error"] is not None
    assert result["title"] == ""
