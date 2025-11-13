"""
手動測試所有命令功能
"""
import sys
sys.path.insert(0, '/Users/shanti/project_base/RuruBot')

from services.commands import process_message

# 測試案例
test_cases = [
    ("雷達", "radar"),
    ("雙子座", "astro"),
    ("金牛座 -w", "astro weekly"),
    ("抽淺草寺", "ticket"),
    ("抽六十甲子籤", "sixty_poem"),
    ("本週國師", "podcast"),
    ("--m", "music"),
    ("--ping 鼠藥", "music with user"),
    ("--help", "help"),
    ("露露 你好", "lulu_chat"),
    ("每日塔羅", "tarot"),
    ("-塔羅 感情運", "tarot with question"),
    ("暈船仔", "dogmeme"),
]

print("=" * 60)
print("命令功能測試")
print("=" * 60)

for text, description in test_cases:
    print(f"\n【測試】{description}")
    print(f"輸入: {text}")

    try:
        result = process_message(text)

        if result:
            print(f"✓ 成功")
            print(f"  類型: {result.get('type')}")
            if result.get('type') == 'text':
                data = result.get('data', '')
                preview = data[:50] + '...' if len(data) > 50 else data
                print(f"  內容: {preview}")
            elif result.get('type') == 'mixed':
                print(f"  資料數量: {len(result.get('data', []))}")
            else:
                print(f"  資料類型: {type(result.get('data'))}")
        else:
            print(f"✗ 返回 None")

    except Exception as e:
        print(f"✗ 錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("測試完成")
print("=" * 60)
