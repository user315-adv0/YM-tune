#!/usr/bin/env python3
"""
Тестовый скрипт для проверки API Яндекс.Музыки
"""

import sys
import os
sys.path.append('backend')

from yandex_client import YandexMusicClient
from config import YA_TOKEN

from yandex_music import Client

def test_user_playlist(playlist_id):
    print(f"\n📝 Тест пользовательского плейлиста {playlist_id}...")
    try:
        client = Client(YA_TOKEN).init()
        playlist = client.users_playlists_list()[0]
        # Попробуем найти нужный плейлист по id
        found = None
        for pl in client.users_playlists_list():
            if pl.kind == playlist_id or pl.uuid == playlist_id:
                found = pl
                break
        if not found:
            print("❌ Плейлист не найден среди пользовательских")
            return False
        tracks = []
        for track_short in found.tracks:
            track = track_short.track
            if not track:
                continue
            download_info = track.get_download_info()
            if not download_info:
                continue
            download_url = download_info[0].get_direct_link()
            tracks.append((track.title, track.artists[0].name if track.artists else "Unknown", download_url))
        if tracks:
            print(f"✅ Получено {len(tracks)} треков из пользовательского плейлиста")
            print(f"📝 Первый трек: {tracks[0][0]} - {tracks[0][1]}")
            print(f"🔗 URL: {tracks[0][2][:50]}...")
            return True
        else:
            print("❌ Нет доступных треков в плейлисте")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_api():
    print("🔍 Тестирование API Яндекс.Музыки...")
    
    if not YA_TOKEN:
        print("❌ Токен не найден в .env файле")
        return False
    
    try:
        client = YandexMusicClient(YA_TOKEN)
        
        # Проверяем подключение
        print("📡 Проверка подключения...")
        if client.test_connection():
            print("✅ Подключение к API успешно")
        else:
            print("❌ Не удалось подключиться к API")
            return False
        
        # Пробуем пользовательский плейлист
        return test_user_playlist("lk.08611572-80bf-43d7-bbcf-a08d76d3d36f")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 API готов к работе!")
        print("🚀 Можно запускать ./start.sh")
    else:
        print("\n💥 API не работает, проверьте токен")
        sys.exit(1) 