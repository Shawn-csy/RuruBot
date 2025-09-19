import requests
import random
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import playlist_provider

load_dotenv()

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.user_access_token = os.getenv("SPOTIFY_USER_ACCESS_TOKEN")  # 用戶授權 token
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
            
            

    def get_user_playlist_track(self) -> Dict[str, Any]:
        """從用戶歌單中獲取隨機歌曲"""
        if not self.user_access_token:
            return {"error": "需要用戶授權才能存取個人歌單"}

        try:
            headers = {
                "Authorization": f"Bearer {self.user_access_token}"
            }

            # 獲取用戶的歌單
            playlists_url = "https://api.spotify.com/v1/me/playlists"
            playlists_response = requests.get(playlists_url, headers=headers, params={"limit": 50})

            if playlists_response.status_code != 200:
                return {"error": f"無法獲取歌單: {playlists_response.status_code}"}

            playlists_data = playlists_response.json()
            playlists = playlists_data.get("items", [])

            if not playlists:
                return {"error": "找不到任何歌單"}

            # 隨機選擇一個歌單
            playlist = random.choice(playlists)
            playlist_id = playlist["id"]

            # 獲取歌單中的歌曲
            tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            tracks_response = requests.get(tracks_url, headers=headers, params={"limit": 100})

            if tracks_response.status_code != 200:
                return {"error": f"無法獲取歌單歌曲: {tracks_response.status_code}"}

            tracks_data = tracks_response.json()
            tracks = tracks_data.get("items", [])

            if not tracks:
                return {"error": "歌單中沒有歌曲"}

            # 隨機選擇一首歌
            track_item = random.choice(tracks)
            track = track_item["track"]

            # 整理回傳資料
            result = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "genre": f"來自歌單: {playlist['name']}",
                "preview_url": track.get("preview_url", ""),
                "external_url": track["external_urls"]["spotify"],
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"]
            }

            return result

        except Exception as e:
            return {"error": f"獲取用戶歌單歌曲時發生錯誤: {str(e)}"}

    def _extract_playlist_id(self, playlist_url: str) -> str:
        """從 Spotify URL 中提取歌單 ID"""
        # 支援各種 Spotify URL 格式
        match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
        if match:
            return match.group(1)
        raise ValueError(f"無法從 URL 中提取歌單 ID: {playlist_url}")

    def _extract_user_id(self, user_url: str) -> str:
        """從 Spotify 用戶 URL 中提取用戶 ID"""
        # 如果已經是純用戶 ID，直接返回
        if not user_url.startswith('http'):
            return user_url

        # 支援各種 Spotify 用戶 URL 格式
        # https://open.spotify.com/user/nightshu?si=...
        # https://open.spotify.com/user/nightshu
        match = re.search(r'user/([a-zA-Z0-9_.-]+)', user_url)
        if match:
            return match.group(1)
        raise ValueError(f"無法從 URL 中提取用戶 ID: {user_url}")

    def get_public_playlist_track(self, playlist_url: str) -> Dict[str, Any]:
        """從公開歌單中獲取隨機歌曲"""
        try:
            token = self._get_access_token()
            playlist_id = self._extract_playlist_id(playlist_url)

            headers = {
                "Authorization": f"Bearer {token}"
            }

            # 獲取歌單資訊
            playlist_info_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
            playlist_info_response = requests.get(playlist_info_url, headers=headers)

            if playlist_info_response.status_code != 200:
                return {"error": f"無法獲取歌單資訊: {playlist_info_response.status_code}"}

            playlist_info = playlist_info_response.json()

            # 獲取歌單中的歌曲
            tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            tracks_response = requests.get(tracks_url, headers=headers, params={"limit": 100})

            if tracks_response.status_code != 200:
                return {"error": f"無法獲取歌單歌曲: {tracks_response.status_code}"}

            tracks_data = tracks_response.json()
            tracks = tracks_data.get("items", [])

            if not tracks:
                return {"error": "歌單中沒有歌曲"}

            # 隨機選擇一首歌
            track_item = random.choice(tracks)
            track = track_item["track"]

            # 整理回傳資料
            result = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "genre": f"來自歌單: {playlist_info['name']}",
                "preview_url": track.get("preview_url", ""),
                "external_url": track["external_urls"]["spotify"],
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"]
            }

            return result

        except Exception as e:
            return {"error": f"獲取公開歌單歌曲時發生錯誤: {str(e)}"}

    def get_user_public_playlists(self, user_id: str) -> List[Dict[str, Any]]:
        """獲取用戶的公開歌單"""
        try:
            token = self._get_access_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }

            url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
            params = {
                "limit": 50  # 獲取最多 50 個歌單
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"無法獲取用戶 {user_id} 的歌單: {response.status_code}")
                return []

            data = response.json()
            playlists = data.get("items", [])

            # 只返回公開的歌單
            public_playlists = [
                playlist for playlist in playlists
                if playlist.get("public", False) and playlist.get("tracks", {}).get("total", 0) > 0
            ]

            return public_playlists

        except Exception as e:
            print(f"獲取用戶公開歌單時發生錯誤: {str(e)}")
            return []

    def get_random_user_playlist_track(self, user_name: str = None) -> Dict[str, Any]:
        """從指定或隨機用戶的隨機公開歌單中獲取隨機歌曲

        Args:
            user_name: 用戶暱稱，如果不指定則隨機選擇
        """
        try:
            if user_name and user_name in playlist_provider:
                # 使用指定的用戶
                user_url = playlist_provider[user_name]
                user_id = self._extract_user_id(user_url)
                source_info = f"來自 {user_name}"
            else:
                # 隨機選擇一個用戶
                if user_name:
                    print(f"找不到用戶 '{user_name}'，使用隨機推薦")

                # 從字典中隨機選擇
                random_user_name = random.choice(list(playlist_provider.keys()))
                user_url = playlist_provider[random_user_name]
                user_id = self._extract_user_id(user_url)
                source_info = f"來自 {random_user_name}"

            # 獲取該用戶的公開歌單
            user_playlists = self.get_user_public_playlists(user_id)

            if not user_playlists:
                # 如果沒有找到公開歌單，返回錯誤
                return {"error": f"用戶 {user_id} 沒有公開歌單"}

            # 隨機選擇一個歌單
            random_playlist = random.choice(user_playlists)
            playlist_id = random_playlist["id"]

            # 獲取歌單中的歌曲
            token = self._get_access_token()
            headers = {
                "Authorization": f"Bearer {token}"
            }

            tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            tracks_response = requests.get(tracks_url, headers=headers, params={"limit": 100})

            if tracks_response.status_code != 200:
                return {"error": f"無法獲取歌單歌曲: {tracks_response.status_code}"}

            tracks_data = tracks_response.json()
            tracks = tracks_data.get("items", [])

            if not tracks:
                return {"error": "歌單中沒有歌曲"}

            # 隨機選擇一首歌
            track_item = random.choice(tracks)
            track = track_item["track"]

            # 整理回傳資料
            result = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "genre": f"{source_info} 的歌單: {random_playlist['name']}",
                "preview_url": track.get("preview_url", ""),
                "external_url": track["external_urls"]["spotify"],
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"]
            }

            return result

        except Exception as e:
            print(f"獲取隨機用戶歌單歌曲時發生錯誤: {str(e)}")
            # 如果失敗，返回錯誤訊息
            return {"error": f"獲取音樂推薦時發生錯誤: {str(e)}"}

    def get_random_recommendation(self, user_name: str = None) -> Dict[str, Any]:
        """推薦一首歌 - 從指定或隨機用戶的隨機公開歌單中選擇

        Args:
            user_name: 用戶暱稱，如果不指定則隨機選擇
        """
        return self.get_random_user_playlist_track(user_name)

# 建立全域實例
spotify_service = SpotifyService()

if __name__ == "__main__":
    print(spotify_service.get_recommendation())