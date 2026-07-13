"""
tests/use_cases/test_radar.py

測試雷達 use case，不打真實外部 API。
"""
import ast
from unittest.mock import patch
from services.use_cases.radar import get_radar_result


def test_no_line_sdk_import():
    """use case 不能 import LINE SDK"""
    import services.use_cases.radar as mod
    source = open(mod.__file__).read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                assert "linebot" not in (name or ""), f"LINE SDK imported: {name}"


def test_returns_urls_on_success():
    urls = ["https://www.cwa.gov.tw/Data/radar/CV1_3600_202401150930.png"]
    with patch("services.use_cases.radar.radar", return_value=urls):
        result = get_radar_result()
    assert result["error"] is None
    assert result["urls"] == urls


def test_returns_error_when_empty():
    with patch("services.use_cases.radar.radar", return_value=[]):
        result = get_radar_result()
    assert result["error"] is not None
    assert result["urls"] == []


def test_returns_error_when_none():
    with patch("services.use_cases.radar.radar", return_value=None):
        result = get_radar_result()
    assert result["error"] is not None
