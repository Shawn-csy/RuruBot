import unittest
from unittest.mock import patch, MagicMock


from services.astro import get_astro_info


class TestAstro(unittest.TestCase):
    
    @patch('services.astro.requests.get')
    def test_get_astro_info_daily(self, mock_get):
        """測試獲取星座日報"""
        # 創建模擬的 response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <div class="TODAY_CONTENT">今日運勢：很好</div>
            <div class="TODAY_WORD">
                <p>愛情運：普通</p>
                <p>財運：不錯</p>
            </div>
        </html>
        """
        mock_get.return_value = mock_response
        
        # 調用函數
        result = get_astro_info("雙子座", "daily")
        
        # 驗證結果
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "今日運勢：很好")
        self.assertEqual(result[1], "愛情運：普通")
        self.assertEqual(result[2], "財運：不錯")
        
        # 驗證 requests.get 被正確調用
        mock_get.assert_called_once()
        self.assertIn("daily_0.php", mock_get.call_args[0][0])
    
    @patch('services.astro.requests.get')
    def test_get_astro_info_weekly(self, mock_get):
        """測試獲取星座週報"""
        # 創建模擬的 response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <div class="TODAY_CONTENT">本週運勢：很好</div>
            <div class="TODAY_WORD">
                <p>愛情運：普通</p>
                <p>財運：不錯</p>
            </div>
        </html>
        """
        mock_get.return_value = mock_response
        
        # 調用函數
        result = get_astro_info("雙子座", "weekly")
        
        # 驗證結果
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "本週運勢：很好")
        
        # 驗證 requests.get 被正確調用
        mock_get.assert_called_once()
        self.assertIn("weekly_1.php", mock_get.call_args[0][0])


if __name__ == '__main__':
    unittest.main() 