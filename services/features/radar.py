from datetime import datetime, timedelta
from typing import List
import requests
import pytz


def radar() -> List[str]:
    """
    獲取中央氣象署雷達回波圖

    圖片 URL 格式: https://www.cwa.gov.tw/Data/radar/CV1_3600_YYYYMMDDHHmm.png
    每 10 分鐘更新一次（整點、10分、20分、30分、40分、50分）

    Returns:
        List[str]: 雷達圖 URL 列表
    """
    try:
        # 獲取當前時間 (使用台灣時區)
        taipei_tz = pytz.timezone('Asia/Taipei')
        now = datetime.now(taipei_tz)

        # 向下取整到最近的 10 分鐘
        # 例如：14:37 -> 14:30, 14:42 -> 14:40
        minute = (now.minute // 10) * 10

        # 考慮到圖片可能有延遲，嘗試當前時間和前一個時間點
        times_to_try = []

        # 當前時間點（向下取整到 10 分鐘）
        current_time = now.replace(minute=minute, second=0, microsecond=0)
        times_to_try.append(current_time)

        # 前一個時間點（10 分鐘前）
        prev_time = current_time - timedelta(minutes=10)
        times_to_try.append(prev_time)

        # 再前一個時間點（20 分鐘前，作為備用）
        prev_prev_time = current_time - timedelta(minutes=20)
        times_to_try.append(prev_prev_time)

        # 嘗試獲取圖片
        for time_point in times_to_try:
            # 生成圖片 URL
            # 格式: CV1_3600_YYYYMMDDHHmm.png
            time_str = time_point.strftime('%Y%m%d%H%M')
            img_url = f'https://www.cwa.gov.tw/Data/radar/CV1_3600_{time_str}.png'

            # 驗證圖片是否存在（發送 HEAD 請求）
            try:
                response = requests.head(img_url, timeout=5)
                if response.status_code == 200:
                    print(f"✓ 找到雷達圖: {time_str}")
                    return [img_url]
            except:
                continue

        # 如果都失敗，返回最新的 URL（即使可能還不存在）
        latest_time = times_to_try[0]
        latest_url = f'https://www.cwa.gov.tw/Data/radar/CV1_3600_{latest_time.strftime("%Y%m%d%H%M")}.png'
        print(f"⚠ 使用最新時間點: {latest_time.strftime('%Y%m%d%H%M')}")
        return [latest_url]

    except Exception as e:
        print(f"獲取雷達圖時發生錯誤: {e}")
        return []