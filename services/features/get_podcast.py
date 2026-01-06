import requests
import re
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
import base64

def get_spotify_access_token(client_id, client_secret):
    """獲取Spotify API的access token"""
    try:
        # 準備認證信息
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        # 請求access token
        token_url = "https://accounts.spotify.com/api/token"
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(token_url, headers=headers, data=data, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            print(f"獲取access token失敗: {response.status_code}")
            print(f"回應內容: {response.text}")
            return None
            
    except Exception as e:
        print(f"獲取access token時發生錯誤: {e}")
        return None

def _parse_release_date(episode):
    """Parse release date for sorting, fallback to minimal date on error."""
    date_str = episode.get('release_date')
    if not date_str:
        return datetime.min
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return datetime.min


def get_podcast():
    """使用Spotify API獲取最新的星座運勢週報"""
    try:
        spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not spotify_client_id or not spotify_client_secret:
            return "Spotify認證信息未設置"
        
        # 取得access token
        access_token = get_spotify_access_token(spotify_client_id, spotify_client_secret)
        
        if not access_token:
            return "無法獲取Spotify access token"
        
        # Spotify API端點
        show_id = os.getenv("SPOTIFY_SHOW_ID")  # 唐綺陽星座運勢週報的show ID
        api_url = f"https://api.spotify.com/v1/shows/{show_id}/episodes"
        
        # 使用認證的API請求
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'limit': 50,  # 獲取最新的50個episode
            'market': 'TW'
        }
        
        print("正在從Spotify API獲取episode列表...")
        response = requests.get(api_url, headers=headers, params=params, timeout=20)
        
        if response.status_code != 200:
            print(f"API請求失敗，狀態碼: {response.status_code}")
            print(f"回應內容: {response.text}")
            return f"無法連接到Spotify API，狀態碼: {response.status_code}"
        
        data = response.json()
        episodes = data.get('items', [])

        # 按發布日期排序，確保取得最新的集數
        episodes = sorted(episodes, key=_parse_release_date, reverse=True)
        
        
        
        # 尋找包含本週提醒/運勢的最新episode
        weekly_reminder_episode = None
        reminder_keywords = [
            "【本週提醒】",
            "【本周提醒】",
            "本週提醒",
            "本周提醒",
            "【本週運勢】",
            "【本周運勢】",
            "本週運勢",
            "本周運勢",
        ]

        for episode in episodes:
            name = episode.get('name', '')
            description = episode.get('description', '')

            # Spotify 上的標題可能有「週/周」或缺少中括號，統一視為提醒/運勢集數
            if any(keyword in name or keyword in description for keyword in reminder_keywords):
                weekly_reminder_episode = episode
                print(f"找到本週運勢/提醒 episode: {name}")
                break

        if not weekly_reminder_episode:
            print("未找到本週運勢/提醒 episode")
            return "國師本週還沒有更新～"
        
        # 提取episode的描述內容和名稱
        episode_description = weekly_reminder_episode.get('description', '')
        episode_name = weekly_reminder_episode.get('name', '')
        
        print(f"Episode名稱: {episode_name}")
        
        
        if episode_description:
            # 清理和格式化內容，傳遞episode名稱作為標題
            formatted_content = format_podcast_content(episode_description, episode_name)
            return formatted_content
        else:
            return "無法獲取episode描述內容"
        
    except Exception as e:
        print(f"獲取podcast時發生錯誤: {e}")
        return f"獲取podcast時發生錯誤: {e}"

def clean_podcast_content(content):
    """清理podcast內容，移除多餘的字符和格式"""
    if not content:
        return ""
    
    # 移除多餘的空白字符
    content = re.sub(r'\s+', ' ', content)
    
    # 移除HTML標籤
    content = re.sub(r'<[^>]+>', '', content)
    
    # 移除多餘的換行符
    content = re.sub(r'\n+', '\n', content)
    
    # 移除開頭和結尾的空白
    content = content.strip()
    
    return content

def format_podcast_content(content, title):
    """格式化podcast內容為標準格式"""
    if not content:
        return "無法解析星座運勢資料"
    
    
    cleaned_content = clean_podcast_content(content)
    if not cleaned_content:
        return "無法解析星座運勢資料"
    
    return extract_from_raw_content(cleaned_content, title)

def extract_from_raw_content(content, title):
    """從原始內容中提取結構化的星座運勢資料"""
    if not content:
        return "無法解析星座運勢資料"
    
    
    
    # 提取完整的標題（包含episode名稱）
    # 尋找本週提醒/運勢開頭的完整標題，直到遇到下一個【】
    # 如果標題已經包含在傳入的title參數中，則直接使用
    normalized_title = title.replace("本周", "本週")
    if "本週提醒" in normalized_title or "本週運勢" in normalized_title:
        final_title = normalized_title
    else:
        title_match = re.search(r'【本[週周](提醒|運勢)】[^【]*', content)
        if not title_match:
            title_match = re.search(r'本[週周](提醒|運勢)[^【]*', content)

        if title_match:
            final_title = title_match.group(0).replace("本周", "本週").strip()
            # 確保標題有括號格式
            if not final_title.startswith("【"):
                final_title = f"【{final_title}】"
            final_title = re.sub(r'\s+', ' ', final_title)
        else:
            final_title = "【本週運勢】"
           
    
    # 提取各個分類的星座運勢
    categories = {
        "累的": [],
        "穩的": [],
        "讚的": []
    }
    
    # 使用正則表達式提取每個分類的內容
    for category in categories.keys():
        pattern = rf'【{category}】([^【]*)'
        match = re.search(pattern, content)
        if match:
            category_content = match.group(1).strip()
          
            
            # 提取星座和對應的運勢
            # 先找到所有星座名稱
            zodiac_signs = ["牡羊", "金牛", "雙子", "巨蟹", "獅子", "處女", "天秤", "天蠍", "射手", "魔羯", "水瓶", "雙魚"]
            
            # 在分類內容中尋找每個星座
            for zodiac in zodiac_signs:
                if zodiac in category_content:
                    # 找到該星座的運勢描述
                    # 使用更精確的正則表達式，確保只匹配當前星座的運勢
                    # 格式：星座：運勢內容（到下一個星座或分類結束）
                    zodiac_pattern = rf'{zodiac}：([^】]+?)(?=\s*[^：\s]+：|$)'
                    zodiac_match = re.search(zodiac_pattern, category_content)
                    if zodiac_match:
                        fortune = zodiac_match.group(1).strip()
                        # 清理運勢內容，移除多餘的空白
                        fortune = re.sub(r'\s+', ' ', fortune).strip()
                        categories[category].append(f"{zodiac}：{fortune}")
                        
    
    # 組合成最終格式
    result_lines = [final_title]
    
    for category, fortunes in categories.items():
        if fortunes:
            result_lines.append(f"【{category}】")
            result_lines.extend(fortunes)
    
    final_result = '\n'.join(result_lines)
    
    
    
    return final_result
