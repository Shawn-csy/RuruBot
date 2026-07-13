"""
tests/use_cases/test_answers_book.py

測試解答之書 use case，不打真實檔案系統（mock feature）。
"""
import ast
from unittest.mock import patch
from services.use_cases.answers_book import get_answers_book_result


def test_no_line_sdk_import():
    import services.use_cases.answers_book as mod
    source = open(mod.__file__).read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for name in names:
                assert "linebot" not in (name or ""), f"LINE SDK imported: {name}"


def test_returns_answer():
    with patch("services.use_cases.answers_book.get_answer", return_value="是的"):
        result = get_answers_book_result("我會成功嗎")
    assert result["error"] is None
    assert result["answer"] == "是的"
    assert result["question"] == "我會成功嗎"


def test_question_empty():
    with patch("services.use_cases.answers_book.get_answer", return_value="不"):
        result = get_answers_book_result("")
    assert result["error"] is None
    assert result["answer"] == "不"


def test_error_on_exception():
    with patch("services.use_cases.answers_book.get_answer", side_effect=Exception("爆了")):
        result = get_answers_book_result("問題")
    assert result["error"] is not None
    assert result["answer"] == ""


def test_required_keys():
    with patch("services.use_cases.answers_book.get_answer", return_value="是的"):
        result = get_answers_book_result("問題")
    for key in ("question", "answer", "error"):
        assert key in result
