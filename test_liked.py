#!/usr/bin/env python3
"""
Тест получения любимых треков
"""

import sys
import os
sys.path.append('backend')

from yandex_client import YandexMusicClient
from config import YA_TOKEN

def test_liked():
    print("❤️ Тестирование получения любимых треков...")
    
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
        
        # Получаем любимые треки
        tracks = client.fetch_liked_tracks()
        
        if tracks:
            print(f"✅ Получено {len(tracks)} любимых треков")
            print(f"📝 Первый трек: {tracks[0].title} - {tracks[0].artist}")
            print(f"🔗 URL: {tracks[0].url[:50]}...")
            return True
        else:
            print("❌ Нет любимых треков или ошибка доступа")
            print("💡 Убедитесь что у вас есть треки в 'Мне нравятся'")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = test_liked()
    if success:
        print("\n🎉 Любимые треки доступны!")
    else:
        print("\n💥 Проблема с получением любимых треков")
        sys.exit(1) 