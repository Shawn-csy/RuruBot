"""
簡單的命令測試 - 只測試解析邏輯，不調用實際 API
"""
import sys
sys.path.insert(0, '/Users/shanti/project_base/RuruBot')

from services.commands import parse_command

# 測試案例
test_cases = [
    ("雷達", "radar", {}),
    ("雙子座", "astro", {"astro_name": "雙子座", "type": "daily"}),
    ("金牛座 -w", "astro", {"astro_name": "金牛座", "type": "weekly"}),
    ("抽淺草寺 想問工作", "ticket", {"text": "抽淺草寺 想問工作"}),
    ("本週國師", "podcast", {}),
    ("--help", "help", {}),
    ("暈船仔", "dogmeme", {}),
    ("解答之書 我會成功嗎", "answers_book", {"question": "我會成功嗎"}),
]

print("=" * 60)
print("命令解析測試")
print("=" * 60)

passed = 0
failed = 0

for text, expected_cmd, expected_params in test_cases:
    print(f"\n輸入: {text}")

    try:
        command, params = parse_command(text)

        if command == expected_cmd:
            # 檢查參數
            params_match = True
            for key, value in expected_params.items():
                if params.get(key) != value:
                    params_match = False
                    print(f"  ✗ 參數不匹配: {key} = {params.get(key)} (預期: {value})")
                    break

            if params_match:
                print(f"  ✓ 通過: {command}")
                passed += 1
            else:
                failed += 1
        else:
            print(f"  ✗ 失敗: 得到 {command} (預期: {expected_cmd})")
            failed += 1

    except Exception as e:
        print(f"  ✗ 錯誤: {str(e)}")
        failed += 1

print("\n" + "=" * 60)
print(f"測試結果: {passed} 通過, {failed} 失敗")
print("=" * 60)
