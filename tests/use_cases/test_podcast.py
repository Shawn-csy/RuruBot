"""
tests/use_cases/test_podcast.py

測試國師運勢 use case，不打真實 Spotify API。
"""
import ast
from unittest.mock import patch
from services.use_cases.podcast import get_podcast_result, _parse_podcast_string

MOCK_PODCAST_STRING = """【本週運勢】2024/1/1
【讚的】
牡羊：本週極佳，適合推進重要事項
金牛：感情順利
【穩的】
雙子：工作平穩
【累的】
巨蟹：需要多休息"""


def test_no_line_sdk_import():
    import services.use_cases.podcast as mod
    source = open(mod.__file__).read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                assert "linebot" not in (name or ""), f"LINE SDK imported: {name}"


def test_parse_podcast_string_title():
    parsed = _parse_podcast_string(MOCK_PODCAST_STRING)
    assert "本週運勢" in parsed["title"]


def test_parse_podcast_string_groups():
    parsed = _parse_podcast_string(MOCK_PODCAST_STRING)
    assert len(parsed["groups"]["讚的"]) == 2
    assert parsed["groups"]["讚的"][0]["sign"] == "牡羊"
    assert len(parsed["groups"]["穩的"]) == 1
    assert len(parsed["groups"]["累的"]) == 1


def test_get_podcast_result_success():
    with patch("services.use_cases.podcast.get_podcast", return_value=MOCK_PODCAST_STRING):
        result = get_podcast_result()
    assert result["error"] is None
    assert "本週運勢" in result["title"]
    assert isinstance(result["groups"], dict)
    assert "讚的" in result["groups"]


def test_get_podcast_result_error_string():
    with patch("services.use_cases.podcast.get_podcast", return_value="國師本週還沒有更新～"):
        result = get_podcast_result()
    assert result["error"] == "國師本週還沒有更新～"
    assert result["title"] == ""


def test_get_podcast_result_empty():
    with patch("services.use_cases.podcast.get_podcast", return_value=""):
        result = get_podcast_result()
    assert result["error"] is not None


def test_result_has_required_keys():
    with patch("services.use_cases.podcast.get_podcast", return_value=MOCK_PODCAST_STRING):
        result = get_podcast_result()
    for key in ("title", "groups", "error"):
        assert key in result
