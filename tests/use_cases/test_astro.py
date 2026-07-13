"""
tests/use_cases/test_astro.py

use case 層不 import LINE SDK，測試不需要 mock FlexMessage。
"""
from unittest.mock import patch
from services.use_cases.astro import get_astro_result, FORTUNE_TYPES


MOCK_RAW_DAILY = [
    "\n金牛座每日運勢\n整體運勢★★★☆☆：今天普通。\n愛情運勢★★★★☆：感情順利。\n事業運勢★★★☆☆：工作穩定。\n財運運勢★★☆☆☆：花費較多。",
    "今天保持平常心。"
]

MOCK_RAW_WEEKLY = [
    "\n金牛座本周運勢\n整體運勢★★★★☆：本週順遂。\n愛情運勢★★★☆☆：感情平穩。\n事業運勢★★★★☆：工作突破。\n財運運勢★★★☆☆：小有收穫。",
    "保持耐心。"
]


class TestGetAstroResult:

    def test_daily_structure(self):
        """回傳 dict 包含所有必要欄位"""
        with patch('services.use_cases.astro.get_astro_info', return_value=MOCK_RAW_DAILY):
            result = get_astro_result("金牛座", "daily")

        assert result["sign"] == "金牛座"
        assert result["fortune_type"] == "daily"
        assert isinstance(result["title"], str) and result["title"]
        assert len(result["fortunes"]) == len(FORTUNE_TYPES)
        for f in result["fortunes"]:
            assert "label" in f
            assert "stars" in f
            assert "content" in f
        assert isinstance(result["reminder"], str) and result["reminder"]
        assert result["error"] is None

    def test_weekly_structure(self):
        with patch('services.use_cases.astro.get_astro_info', return_value=MOCK_RAW_WEEKLY):
            result = get_astro_result("金牛座", "weekly")

        assert result["sign"] == "金牛座"
        assert result["fortune_type"] == "weekly"
        assert result["error"] is None

    def test_fortunes_parsed(self):
        """fortunes 正確解析星星數量、label、內容"""
        with patch('services.use_cases.astro.get_astro_info', return_value=MOCK_RAW_DAILY):
            result = get_astro_result("金牛座", "daily")

        fortunes = result["fortunes"]
        assert fortunes[0]["label"] == "整體運勢"
        assert fortunes[0]["stars"] == 3
        assert "今天普通" in fortunes[0]["content"]

        assert fortunes[1]["label"] == "愛情運勢"
        assert fortunes[1]["stars"] == 4

        assert fortunes[2]["label"] == "事業運勢"
        assert fortunes[2]["stars"] == 3

        assert fortunes[3]["label"] == "財運運勢"
        assert fortunes[3]["stars"] == 2

    def test_reminder_from_second_element(self):
        with patch('services.use_cases.astro.get_astro_info', return_value=MOCK_RAW_DAILY):
            result = get_astro_result("金牛座", "daily")
        assert result["reminder"] == "今天保持平常心。"

    def test_title_contains_sign(self):
        with patch('services.use_cases.astro.get_astro_info', return_value=MOCK_RAW_DAILY):
            result = get_astro_result("金牛座", "daily")
        assert "金牛座" in result["title"] or "運勢" in result["title"]

    def test_empty_raw_returns_error(self):
        """外部 API 回空資料時，error 欄位有值，fortunes 仍有完整結構"""
        with patch('services.use_cases.astro.get_astro_info', return_value=[]):
            result = get_astro_result("金牛座", "daily")

        assert result["error"] is not None
        assert len(result["fortunes"]) == len(FORTUNE_TYPES)
        for f in result["fortunes"]:
            assert f["stars"] == 0

    def test_none_raw_returns_error(self):
        with patch('services.use_cases.astro.get_astro_info', return_value=None):
            result = get_astro_result("金牛座", "daily")

        assert result["error"] is not None

    def test_no_line_sdk_import(self):
        """use case 不應 import LINE SDK"""
        import services.use_cases.astro as uc
        import sys
        line_modules = [k for k in sys.modules if k.startswith("linebot")]
        # 即使 linebot 在 sys.modules（其他 module 用到），
        # use case 自身不應直接 import 它
        import ast, inspect
        source = inspect.getsource(uc)
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in getattr(node, 'names', []):
                    assert not alias.name.startswith('linebot'), \
                        f"use case 不應 import linebot，但發現: {alias.name}"
                if hasattr(node, 'module') and node.module:
                    assert not node.module.startswith('linebot'), \
                        f"use case 不應 import linebot，但發現: {node.module}"
