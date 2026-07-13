#!/usr/bin/env python3
"""測試每日梗圖指令"""

from services.commands.config import COMMAND_CONFIG
from services.commands.processor import process_message

def test_daily_meme_command():
    """測試每日梗圖指令"""
    test_messages = [
        "每日梗圖",
        "今日梗圖",
        "每日迷因"
    ]

    for msg in test_messages:
        print(f"\n{'='*50}")
        print(f"測試指令: {msg}")
        print(f"{'='*50}")

        result = process_message(msg)

        if result:
            print(f"✓ 指令識別成功")
            print(f"回應類型: {result.get('type')}")

            if result.get('type') == 'mixed':
                images = result.get('data', [])
                print(f"圖片數量: {len(images)}")
                for i, img in enumerate(images, 1):
                    print(f"  {i}. {img.get('url')}")
            elif result.get('type') == 'text':
                print(f"文字回應: {result.get('data')}")
        else:
            print(f"✗ 指令未被識別")

if __name__ == "__main__":
    test_daily_meme_command()
