from yandex_music import Client
from typing import List
from models import Track
import requests

class YandexMusicClient:
    def __init__(self, token: str):
        self.client = Client(token).init()
    
    def get_best_quality_url(self, download_info) -> str:
        """Выбирает лучшее качество по битрейту"""
        if not download_info:
            return None
        
        # Сортируем по битрейту (лучшее качество первым)
        sorted_info = sorted(download_info, key=lambda x: x.bitrate_in_kbps, reverse=True)
        
        # Логируем доступные качества
        print(f"  📊 Доступные качества:")
        for i, info in enumerate(sorted_info):
            print(f"    {i}: {info.bitrate_in_kbps}kbps, {info.codec}")
        
        # Возвращаем лучшее качество
        best_url = sorted_info[0].get_direct_link()
        print(f"  ✅ Выбрано: {sorted_info[0].bitrate_in_kbps}kbps")
        return best_url
    
    def fetch_tracks_universal(self, source_id: str) -> List[Track]:
        """Универсальная функция для получения треков из любого источника"""
        try:
            tracks = []
            
            # "Мне нравятся"
            if source_id.lower() == "liked":
                return self.fetch_liked_tracks()
            
            # Альбом (числовой ID)
            if source_id.isdigit():
                return self.fetch_album_tracks(source_id)
            
            # Плейлист (числовой ID)
            if source_id.isdigit():
                return self.fetch_playlist_tracks(source_id)
            
            # Персональный плейлист (lk.xxx)
            if source_id.startswith("lk."):
                return self.fetch_personal_playlist_tracks(source_id)
            
            # Попробуем как плейлист
            return self.fetch_playlist_tracks(source_id)
            
        except Exception as e:
            print(f"Ошибка при получении треков из {source_id}: {e}")
            return []
    
    def fetch_album_tracks(self, album_id: str) -> List[Track]:
        """Получает треки альбома"""
        try:
            album = self.client.albums_with_tracks(album_id)
            if not album or not album.volumes:
                return []
            
            tracks = []
            for volume in album.volumes:
                for track in volume:
                    try:
                        download_info = track.get_download_info()
                        if not download_info:
                            continue
                        
                        print(f"🎵 Трек '{track.title}':")
                        download_url = self.get_best_quality_url(download_info)
                        if not download_url:
                            continue
                        
                        tracks.append(Track(
                            title=track.title,
                            artist=track.artists[0].name if track.artists else "Unknown",
                            url=download_url,
                            duration=track.duration_ms // 1000
                        ))
                    except Exception as e:
                        print(f"⚠️ Ошибка при обработке трека альбома: {e}")
                        continue
            
            return tracks
            
        except Exception as e:
            print(f"Ошибка при получении альбома: {e}")
            return []
    
    def fetch_personal_playlist_tracks(self, playlist_id: str) -> List[Track]:
        """Получает треки персонального плейлиста"""
        try:
            # Получаем все плейлисты пользователя
            playlists = self.client.users_playlists_list()
            
            # Ищем нужный плейлист
            target_playlist = None
            for playlist in playlists:
                if (hasattr(playlist, 'uuid') and playlist.uuid == playlist_id) or \
                   (hasattr(playlist, 'kind') and str(playlist.kind) == playlist_id):
                    target_playlist = playlist
                    break
            
            if not target_playlist:
                print(f"Плейлист {playlist_id} не найден")
                return []
            
            tracks = []
            for track_short in target_playlist.tracks:
                try:
                    track = track_short.track
                    if not track:
                        continue
                    
                    download_info = track.get_download_info()
                    if not download_info:
                        continue
                    
                    download_url = self.get_best_quality_url(download_info)
                    if not download_url:
                        continue
                    
                    tracks.append(Track(
                        title=track.title,
                        artist=track.artists[0].name if track.artists else "Unknown",
                        url=download_url,
                        duration=track.duration_ms // 1000
                    ))
                except Exception as e:
                    print(f"⚠️ Ошибка при обработке трека плейлиста: {e}")
                    continue
            
            return tracks
            
        except Exception as e:
            print(f"Ошибка при получении персонального плейлиста: {e}")
            return []
    
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
                
                # Выбираем лучшее качество
                download_url = self.get_best_quality_url(download_info)
                if not download_url:
                    continue
                
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
    
    def fetch_liked_tracks(self) -> List[Track]:
        """Получает треки из 'Мне нравятся' с прямыми URL для скачивания"""
        try:
            # Получаем треки из "Мне нравятся"
            liked_tracks = self.client.users_likes_tracks()
            tracks = []
            
            for track_short in liked_tracks:
                try:
                    # Получаем полную информацию о треке
                    track = track_short.track
                    
                    # Проверяем что трек доступен
                    if not track:
                        continue
                    
                    # Получаем информацию для скачивания
                    download_info = track.get_download_info()
                    if not download_info:
                        print(f"⚠️ Трек '{track.title}' недоступен для скачивания")
                        continue
                    
                    # Выбираем лучшее качество
                    download_url = self.get_best_quality_url(download_info)
                    if not download_url:
                        continue
                    
                    tracks.append(Track(
                        title=track.title,
                        artist=track.artists[0].name if track.artists else "Unknown",
                        url=download_url,
                        duration=track.duration_ms // 1000  # конвертируем в секунды
                    ))
                except Exception as e:
                    print(f"⚠️ Ошибка при обработке трека: {e}")
                    continue
            
            return tracks
            
        except Exception as e:
            print(f"Ошибка при получении любимых треков: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Проверяет подключение к API"""
        try:
            account = self.client.account_status()
            return True
        except:
            return False 