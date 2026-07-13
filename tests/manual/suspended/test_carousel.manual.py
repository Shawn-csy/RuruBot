#!/usr/bin/env python3
"""測試圖片輪播功能"""

from services.commands.processor import process_message
from services.message_builder import build_messages_from_result

def test_carousel():
    """測試每日梗圖輪播"""
    print("=" * 60)
    print("測試每日梗圖輪播功能")
    print("=" * 60)

    # 處理指令
    result = process_message("每日梗圖")

    if result:
        print(f"\n✓ 指令識別成功")
        print(f"回應類型: {result.get('type')}")

        # 構建 LINE 訊息
        messages = build_messages_from_result(result)

        if messages:
            print(f"\n✓ 訊息構建成功")
            print(f"訊息數量: {len(messages)}")

            for i, msg in enumerate(messages, 1):
                print(f"\n訊息 {i}:")
                print(f"  類型: {type(msg).__name__}")

                if hasattr(msg, 'alt_text'):
                    print(f"  Alt Text: {msg.alt_text}")

                if hasattr(msg, 'template'):
                    template = msg.template
                    print(f"  Template 類型: {type(template).__name__}")

                    if hasattr(template, 'columns'):
                        columns = template.columns
                        print(f"  欄位數量: {len(columns)}")

                        # 顯示前 3 個欄位的資訊
                        for j, col in enumerate(columns[:3], 1):
                            print(f"\n  欄位 {j}:")
                            if hasattr(col, 'image_url'):
                                print(f"    圖片 URL: {col.image_url}")
                            if hasattr(col, 'action'):
                                print(f"    動作標籤: {col.action.label}")

                        if len(columns) > 3:
                            print(f"\n  ... 還有 {len(columns) - 3} 個欄位")

        else:
            print("✗ 訊息構建失敗")
    else:
        print("✗ 指令未被識別")

if __name__ == "__main__":
    test_carousel()
