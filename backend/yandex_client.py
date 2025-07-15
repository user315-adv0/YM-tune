from yandex_music import Client
from typing import List
from models import Track
import requests

class YandexMusicClient:
    def __init__(self, token: str):
        self.client = Client(token).init()
    
    def fetch_playlist_tracks(self, playlist_id: str) -> List[Track]:
        """Получает треки плейлиста с прямыми URL для скачивания"""
        try:
            # Получаем плейлист
            playlist = self.client.users_playlists(playlist_id)
            tracks = []
            
            for track_short in playlist.tracks:
                # Получаем полную информацию о треке
                track = track_short.track
                
                # Получаем информацию для скачивания
                download_info = track.get_download_info()
                if not download_info:
                    continue
                
                # Берем первое доступное качество
                download_url = download_info[0].get_direct_link()
                
                tracks.append(Track(
                    title=track.title,
                    artist=track.artists[0].name if track.artists else "Unknown",
                    url=download_url,
                    duration=track.duration_ms // 1000  # конвертируем в секунды
                ))
            
            return tracks
            
        except Exception as e:
            print(f"Ошибка при получении плейлиста: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Проверяет подключение к API"""
        try:
            account = self.client.account_status()
            return True
        except:
            return False 