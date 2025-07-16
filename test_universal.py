#!/usr/bin/env python3
"""
Тест универсального endpoint
"""

import sys
import os
sys.path.append('backend')

from yandex_client import YandexMusicClient
from config import YA_TOKEN

def test_universal():
    print("🔍 Тестирование универсального endpoint...")
    
    if not YA_TOKEN:
        print("❌ Токен не найден")
        return False
    
    try:
        client = YandexMusicClient(YA_TOKEN)
        
        # Проверяем подключение
        if not client.test_connection():
            print("❌ Не удалось подключиться к API")
            return False
        
        print("✅ Подключение к API успешно")
        
        # Тест 1: Альбом
        print("\n🎼 Тест альбома 7935690...")
        tracks = client.fetch_tracks_universal("7935690")
        if tracks:
            print(f"✅ Альбом: {len(tracks)} треков")
        else:
            print("❌ Альбом не найден")
        
        # Тест 2: Любимые треки
        print("\n❤️ Тест любимых треков...")
        tracks = client.fetch_tracks_universal("liked")
        if tracks:
            print(f"✅ Любимые: {len(tracks)} треков")
        else:
            print("❌ Любимые треки не найдены")
        
        # Тест 3: Персональный плейлист
        print("\n📝 Тест персонального плейлиста...")
        tracks = client.fetch_tracks_universal("lk.08611572-80bf-43d7-bbcf-a08d76d3d36f")
        if tracks:
            print(f"✅ Плейлист: {len(tracks)} треков")
        else:
            print("❌ Плейлист не найден")
        
        return True
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_universal()
    if success:
        print("\n🎉 Универсальный endpoint готов!")
    else:
        print("\n💥 Проблема с универсальным endpoint")
        sys.exit(1) 