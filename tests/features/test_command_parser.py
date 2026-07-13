import pytest
from services.commands.parsers import parse_astro_params, parse_astro_weekly_flag_params
from services.commands.processor import parse_command


class TestParseAstroParams:
    """parse_astro_params：星座名在前"""

    def test_daily(self):
        result = parse_astro_params("牡羊座")
        assert result == {"astro_name": "牡羊座", "type": "daily"}

    def test_weekly_flag_after(self):
        result = parse_astro_params("牡羊座-w")
        assert result == {"astro_name": "牡羊座", "type": "weekly"}

    def test_weekly_flag_after_space(self):
        result = parse_astro_params("牡羊座 -w")
        assert result == {"astro_name": "牡羊座", "type": "weekly"}

    def test_no_match(self):
        result = parse_astro_params("-w")
        assert result is None

    def test_all_signs(self):
        signs = ["牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座",
                 "天秤座", "天蠍座", "射手座", "魔羯座", "水瓶座", "雙魚座"]
        for sign in signs:
            result = parse_astro_params(sign)
            assert result is not None
            assert result["astro_name"] == sign
            assert result["type"] == "daily"


class TestParseAstroWeeklyFlagParams:
    """parse_astro_weekly_flag_params：-w 在前"""

    def test_flag_before_sign(self):
        result = parse_astro_weekly_flag_params("-w 牡羊座")
        assert result == {"astro_name": "牡羊座", "type": "weekly"}

    def test_flag_before_no_space(self):
        result = parse_astro_weekly_flag_params("-w牡羊座")
        assert result == {"astro_name": "牡羊座", "type": "weekly"}

    def test_no_sign(self):
        result = parse_astro_weekly_flag_params("-w")
        assert result is None



class TestParseCommandAstro:
    """parse_command 端對端：確認 -w 路由正確"""

    def test_sign_only(self):
        cmd, params = parse_command("牡羊座")
        assert cmd == "astro"
        assert params["type"] == "daily"

    def test_sign_then_flag(self):
        cmd, params = parse_command("牡羊座 -w")
        assert cmd == "astro"
        assert params["type"] == "weekly"

    def test_flag_then_sign(self):
        cmd, params = parse_command("-w 牡羊座")
        assert cmd == "astro_weekly"
        assert params["astro_name"] == "牡羊座"
        assert params["type"] == "weekly"

    def test_flag_only_no_sign(self):
        cmd, params = parse_command("-w")
        assert cmd is None

    def test_weekly_returns_same_handler(self):
        """astro 和 astro_weekly 應指向同一個 handler"""
        from services.commands.config import COMMAND_CONFIG
        assert COMMAND_CONFIG["astro"]["handler"] is COMMAND_CONFIG["astro_weekly"]["handler"]
