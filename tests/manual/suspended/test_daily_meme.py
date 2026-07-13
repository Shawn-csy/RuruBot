"""
tests/use_cases/test_daily_meme.py

測試每日梗圖 use case，不打真實外部 API。
"""
import ast
import importlib
from unittest.mock import patch
from services.use_cases.daily_meme import get_daily_meme_result


def test_no_line_sdk_import():
    """use case 不能 import LINE SDK"""
    import services.use_cases.daily_meme as mod
    source = open(mod.__file__).read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                assert "linebot" not in (name or ""), f"LINE SDK imported: {name}"


def test_returns_urls_on_success():
    urls = ["https://images.plurk.com/a.png", "https://images.plurk.com/b.png"]
    with patch("services.use_cases.daily_meme.get_daily_meme", return_value=urls):
        result = get_daily_meme_result()
    assert result["error"] is None
    assert result["urls"] == urls
    assert "/" in result["date_str"]


def test_returns_error_when_no_urls():
    with patch("services.use_cases.daily_meme.get_daily_meme", return_value=None):
        result = get_daily_meme_result()
    assert result["error"] is not None
    assert result["urls"] == []


def test_returns_error_when_empty_list():
    with patch("services.use_cases.daily_meme.get_daily_meme", return_value=[]):
        result = get_daily_meme_result()
    assert result["error"] is not None
    assert result["urls"] == []


def test_date_str_format():
    urls = ["https://images.plurk.com/a.png"]
    with patch("services.use_cases.daily_meme.get_daily_meme", return_value=urls):
        result = get_daily_meme_result()
    # format: YYYY/MM/DD
    parts = result["date_str"].split("/")
    assert len(parts) == 3
    assert len(parts[0]) == 4  # year
