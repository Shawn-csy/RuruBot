import requests
import random
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.access_token = None
        
    def _get_access_token(self) -> str:
        """獲取 Spotify access token"""
        # 檢查環境變數
        if not self.client_id or not self.client_secret:
            raise Exception("SPOTIFY_CLIENT_ID 或 SPOTIFY_CLIENT_SECRET 環境變數未設定")
            
        if self.access_token:
            return self.access_token
            
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()  # 檢查 HTTP 錯誤
            
            token_data = response.json()
            
            if "access_token" not in token_data:
                error_msg = token_data.get("error_description", "未知錯誤")
                raise Exception(f"Spotify API 錯誤: {error_msg}")
                
            self.access_token = token_data["access_token"]
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"網路請求錯誤: {str(e)}")
        except Exception as e:
            raise Exception(f"獲取 access token 失敗: {str(e)}")
        
    def get_genres(self) -> List[str]:
        """獲取所有可用的音樂類型"""
        try:
            token = self._get_access_token()
            url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            genres = data.get("genres", [])
            
            # 如果 API 返回的類型太少，使用預設的常見類型
            if len(genres) < 10:
                genres = [
                    "pop", "rock", "hip-hop", "r-n-b", "electronic", 
                    "jazz", "classical", "country", "reggae", "blues",
                    "indie", "alternative", "folk", "soul", "funk"
                ]
            
            return genres
            
        except Exception as e:
            print(f"獲取音樂類型時發生錯誤: {str(e)}")
            # 返回預設的音樂類型作為備用
            return [
                "pop", "rock", "hip-hop", "r-n-b", "electronic", 
                "jazz", "classical", "country", "reggae", "blues"
            ]
            
    def get_recommendation(self, genre: str = None) -> Dict[str, Any]:
        """獲取音樂推薦"""
        try:
            token = self._get_access_token()
            
            # 使用 search API 搜尋熱門歌曲
            url = "https://api.spotify.com/v1/search"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # 隨機選擇一些搜尋詞
            search_terms = [
                "top hits", "popular songs", "trending", "viral", 
                "chart toppers", "best songs", "hits", "popular music"
            ]
            search_term = random.choice(search_terms)
            
            params = {
                "q": search_term,
                "type": "track",
                "limit": 10,  # 獲取更多結果以便隨機選擇
                "market": "TW"  # 使用台灣市場
            }
            
            print(f"搜尋詞: {search_term}")
            print(f"請求 URL: {url}")
            print(f"請求參數: {params}")
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"API 回應狀態碼: {response.status_code}")
                print(f"API 回應內容: {response.text}")
                return {"error": f"Spotify API 錯誤: {response.status_code}"}
                
            data = response.json()
            
            if "tracks" not in data or "items" not in data["tracks"] or not data["tracks"]["items"]:
                return {"error": "無法獲取推薦歌曲"}
            
            # 從搜尋結果中隨機選擇一首歌
            tracks = data["tracks"]["items"]
            track = random.choice(tracks)
            
            # 整理回傳資料
            result = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "genre": "隨機推薦",
                "preview_url": track.get("preview_url", ""),
                "external_url": track["external_urls"]["spotify"],
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"]
            }
            
            return result
            
        except Exception as e:
            return {"error": f"獲取音樂推薦時發生錯誤: {str(e)}"}
            
    def get_random_recommendation(self) -> Dict[str, Any]:
        """隨機推薦一首歌"""
        return self.get_recommendation()

# 建立全域實例
spotify_service = SpotifyService()

if __name__ == "__main__":
    print(spotify_service.get_recommendation())