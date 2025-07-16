import requests
import json

def test_backend():
    print("🔍 Тестирую backend...")
    
    # Тест 1: Health check
    response = requests.get("http://localhost:8000/health")
    print(f"✅ Health: {response.status_code} - {response.json()}")
    
    # Тест 2: Получение треков
    response = requests.get("http://localhost:8000/tracks/7935690")
    print(f"✅ Треки: {response.status_code}")
    
    if response.status_code == 200:
        tracks = response.json()
        print(f"📊 Найдено треков: {len(tracks)}")
        
        if tracks:
            first_track = tracks[0]
            print(f"🎵 Первый трек: {first_track['title']} - {first_track['artist']}")
            print(f"🔗 URL: {first_track['url'][:100]}...")
            
            # Тест 3: Прокси
            proxy_url = first_track['url']
            print(f"🔍 Тестирую прокси: {proxy_url[:100]}...")
            
            try:
                response = requests.get(f"http://localhost:8000{proxy_url}", timeout=10)
                print(f"📡 Прокси статус: {response.status_code}")
                print(f"📦 Размер: {len(response.content)} байт")
                print(f"🎵 Content-Type: {response.headers.get('content-type')}")
                
                if response.status_code == 200:
                    # Сохраняем первые 1KB для анализа
                    with open('/tmp/frontend_test.mp3', 'wb') as f:
                        f.write(response.content[:1024])
                    print("💾 Сохранено в /tmp/frontend_test.mp3")
                else:
                    print(f"❌ Ошибка: {response.content[:200]}")
                    
            except Exception as e:
                print(f"❌ Ошибка прокси: {str(e)}")
    
    # Тест 4: Фронтенд
    print("\n🌐 Тестирую фронтенд...")
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        print(f"✅ Фронтенд: {response.status_code}")
    except Exception as e:
        print(f"❌ Фронтенд недоступен: {str(e)}")

if __name__ == "__main__":
    test_backend() 