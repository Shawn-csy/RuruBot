"""
每日梗圖功能

從 Plurk LotusMartus 帳號爬取當日的梗圖
"""
import re
from datetime import datetime
from typing import List, Optional
import pytz
from services.features.plurk_image import plurk


def get_daily_meme() -> Optional[List[str]]:
    """
    獲取今日梗圖 URL 列表

    從 LotusMartus 的 Plurk 帳號中尋找今天發布的梗圖貼文,
    並提取所有圖片 URL

    Returns:
        List[str]: 圖片 URL 列表,如果找不到則返回 None
    """
    try:
        # 獲取台灣時間的今日日期 (格式: 1113)
        taipei_tz = pytz.timezone('Asia/Taipei')
        today = datetime.now(taipei_tz)
        date_str = today.strftime("%-m%-d")

        print(f"[每日梗圖] 搜尋日期: {date_str}")

        # 獲取 LotusMartus 的用戶資料
        profile = plurk.callAPI('/APP/Profile/getPublicProfile', {
            'user_id': 'LotusMartus'
        })

        user_id = profile.get('user_info', {}).get('id')
        if not user_id:
            print("[每日梗圖] 無法取得用戶 ID")
            return None

        # 獲取最近的貼文
        result = plurk.callAPI('/APP/Timeline/getPlurks', {
            'user_id': user_id,
            'limit': 50  # 取最近 50 則貼文
        })

        # 找出今天的貼文 (開頭為日期,例如: 1113)
        today_plurk = None
        for p in result.get('plurks', []):
            content_raw = p.get('content_raw', '')
            if content_raw.startswith(date_str):
                today_plurk = p
                print(f"[每日梗圖] ✓ 找到今日貼文")
                break

        if not today_plurk:
            print(f"[每日梗圖] ✗ 未找到 {date_str} 的貼文")
            return None

        # 從貼文內容中提取所有圖片 URL
        content_raw = today_plurk.get('content_raw', '')

        # Plurk 圖片 URL 格式: https://images.plurk.com/xxx.png
        image_pattern = r'https://images\.plurk\.com/[^\s<>"\)]+\.(png|jpg|jpeg|gif)'
        image_urls = [m.group(0) for m in re.finditer(image_pattern, content_raw)]

        print(f"[每日梗圖] 主貼文找到 {len(image_urls)} 張圖片")

        # 獲取回應中的圖片 (只取 LotusMartus 自己的回應)
        try:
            plurk_id = today_plurk.get('plurk_id')
            responses = plurk.callAPI('/APP/Responses/get', {
                'plurk_id': plurk_id,
                'limit': 100
            })

            # 從回應中提取圖片 (只取帳號主人的回應)
            response_images = []
            owner_response_count = 0
            for resp in responses.get('responses', []):
                resp_user_id = resp.get('user_id')
                # 只處理 LotusMartus (user_id: 4473602) 的回應
                if resp_user_id == user_id:
                    owner_response_count += 1
                    resp_content = resp.get('content_raw', '')
                    resp_imgs = [m.group(0) for m in re.finditer(image_pattern, resp_content)]
                    response_images.extend(resp_imgs)

            print(f"[每日梗圖] LotusMartus 自己的回應: {owner_response_count} 則")
            print(f"[每日梗圖] 回應中找到 {len(response_images)} 張圖片")

            # 合併主貼文和回應中的所有圖片
            all_images = image_urls + response_images
            print(f"[每日梗圖] 總共 {len(all_images)} 張圖片")

            return all_images if all_images else None

        except Exception as e:
            print(f"[每日梗圖] 獲取回應時發生錯誤: {e}")
            # 即使獲取回應失敗,至少返回主貼文的圖片
            return image_urls if image_urls else None

    except Exception as e:
        print(f"[每日梗圖] 錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None
