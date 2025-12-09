#!/usr/bin/env python3
"""測試 Plurk API 爬取 LotusMartus 的每日梗圖"""

import os
import json
from datetime import datetime
import pytz
from dotenv import load_dotenv
from plurk_oauth import PlurkAPI

load_dotenv()

# Plurk API 設定
CONSUMER_KEY = os.getenv('plurk_App_key')
CONSUMER_SECRET = os.getenv('plurk_App_secret')
ACCESS_TOKEN = os.getenv('plurk_token')
ACCESS_TOKEN_SECRET = os.getenv('plurk_secret')

# 初始化 Plurk API
plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)
plurk.authorize(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def test_get_user_info():
    """測試獲取用戶資料"""
    print("=== 測試獲取 LotusMartus 用戶資料 ===")
    try:
        # 根據用戶名獲取用戶資料
        result = plurk.callAPI('/APP/Profile/getPublicProfile', {
            'user_id': 'LotusMartus'
        })
        print(f"用戶資料: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    except Exception as e:
        print(f"錯誤: {e}")
        return None

def test_get_plurks():
    """測試獲取用戶的 Plurks"""
    print("\n=== 測試獲取 LotusMartus 的 Plurks ===")
    try:
        # 先獲取用戶資料以取得 user_id
        profile = plurk.callAPI('/APP/Profile/getPublicProfile', {
            'user_id': 'LotusMartus'
        })

        user_id = profile.get('user_info', {}).get('id')
        print(f"User ID: {user_id}")

        # 獲取用戶的 Plurks
        result = plurk.callAPI('/APP/Timeline/getPlurks', {
            'user_id': user_id,
            'limit': 10  # 取最近 10 則
        })

        print(f"\n找到 {len(result.get('plurks', []))} 則 Plurks")

        # 顯示每則 Plurk 的基本資訊
        for i, p in enumerate(result.get('plurks', []), 1):
            print(f"\n--- Plurk {i} ---")
            print(f"ID: {p.get('plurk_id')}")
            print(f"內容: {p.get('content_raw', '')[:100]}")
            print(f"發布時間: {p.get('posted')}")

        return result
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_get_today_meme():
    """測試獲取今日梗圖"""
    print("\n=== 測試獲取今日梗圖 ===")
    try:
        # 獲取台灣時間的今日日期
        taipei_tz = pytz.timezone('Asia/Taipei')
        today = datetime.now(taipei_tz)
        date_str = today.strftime("%-m%-d")  # 格式: 1113 (月日連在一起)

        print(f"搜尋日期: {date_str}")

        # 獲取用戶資料
        profile = plurk.callAPI('/APP/Profile/getPublicProfile', {
            'user_id': 'LotusMartus'
        })
        user_id = profile.get('user_info', {}).get('id')

        # 獲取最近的 Plurks (增加數量)
        result = plurk.callAPI('/APP/Timeline/getPlurks', {
            'user_id': user_id,
            'limit': 50  # 增加到 50 則
        })

        # 顯示所有貼文開頭 (除錯用)
        print(f"\n所有貼文預覽:")
        for i, p in enumerate(result.get('plurks', [])[:10], 1):
            content = p.get('content_raw', '')
            print(f"{i}. {content[:50]}...")

        # 找出今天的貼文
        today_plurk = None
        for p in result.get('plurks', []):
            content = p.get('content_raw', '')
            # 檢查是否以日期開頭 (例如: 1113)
            if content.startswith(date_str):
                today_plurk = p
                print(f"\n✓ 找到今日貼文!")
                print(f"內容預覽: {content[:200]}")
                break

        if not today_plurk:
            print(f"\n✗ 未找到包含 {date_str} 的貼文")
            print(f"提示: 可能今天還沒發布,或是日期格式不同")
            return None

        # 提取圖片 URL
        print(f"\n=== 提取圖片 URL ===")
        content = today_plurk.get('content', '')
        content_raw = today_plurk.get('content_raw', '')

        print(f"\n完整內容預覽 (content_raw):")
        print(f"{content_raw[:1000]}")
        print(f"\n... (共 {len(content_raw)} 字元)")

        # 從內容中提取所有圖片 URL
        import re
        # Plurk 圖片格式通常是 https://images.plurk.com/xxx.png 或 .jpg
        image_pattern = r'https://images\.plurk\.com/[^\s<>"\)]+\.(png|jpg|jpeg|gif)'
        images = re.findall(image_pattern, content_raw)

        # 提取完整 URL
        image_urls = [match[0] if isinstance(match, tuple) else match
                      for match in re.finditer(image_pattern, content_raw)]
        image_urls = [m.group(0) for m in image_urls]

        print(f"\n找到 {len(image_urls)} 張圖片:")
        for i, url in enumerate(image_urls, 1):
            print(f"{i}. {url}")

        # 檢查是否有回應(responses)包含更多圖片
        plurk_id = today_plurk.get('plurk_id')
        print(f"\n=== 檢查回應中的圖片 ===")
        print(f"Plurk ID: {plurk_id}")

        try:
            responses = plurk.callAPI('/APP/Responses/get', {
                'plurk_id': plurk_id,
                'limit': 100
            })

            response_count = len(responses.get('responses', []))
            print(f"找到 {response_count} 則回應")

            # 查看回應的結構
            print(f"\n=== 前 3 則回應的資訊 ===")
            for i, resp in enumerate(responses.get('responses', [])[:3], 1):
                print(f"\n回應 {i}:")
                print(f"  user_id: {resp.get('user_id')}")
                print(f"  內容: {resp.get('content_raw', '')[:100]}")

            # 從回應中提取圖片 (只取 LotusMartus 的回應)
            response_images = []
            lotusartus_response_count = 0
            for resp in responses.get('responses', []):
                resp_user_id = resp.get('user_id')
                # 只處理 user_id 為 4473602 (LotusMartus) 的回應
                if resp_user_id == user_id:
                    lotusartus_response_count += 1
                    resp_content = resp.get('content_raw', '')
                    resp_imgs = [m.group(0) for m in re.finditer(image_pattern, resp_content)]
                    response_images.extend(resp_imgs)

            print(f"\n✓ LotusMartus 自己的回應: {lotusartus_response_count} 則")

            if response_images:
                print(f"\n回應中找到 {len(response_images)} 張圖片:")
                for i, url in enumerate(response_images, 1):
                    print(f"{i}. {url}")

                # 合併所有圖片
                all_images = image_urls + response_images
                print(f"\n總共: {len(all_images)} 張圖片")
                return all_images
            else:
                print("回應中沒有圖片")

        except Exception as e:
            print(f"獲取回應時發生錯誤: {e}")

        return image_urls

    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # test_get_user_info()
    # test_get_plurks()
    test_get_today_meme()
