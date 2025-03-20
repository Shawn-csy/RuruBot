import pytest
import os

def run_tests():
    """執行所有測試"""
    # 獲取測試目錄的路徑
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 執行測試並收集結果
    result = pytest.main([
        "-v",                     # 詳細輸出
        "--tb=short",            # 簡短的錯誤追蹤
        test_dir                  # 測試目錄
    ])
    
    return result == 0  # 0 表示所有測試通過

if __name__ == "__main__":
    success = run_tests()
    print("測試" + ("成功" if success else "失敗")) 