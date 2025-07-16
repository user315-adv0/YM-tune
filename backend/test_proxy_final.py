import requests
import urllib.parse

def test_proxy_final():
    # Полный URL из теста токена
    url = "https://api.music.yandex.net/get-mp3/bd396a54920ca3b71108c68f44153aa8/19812475258/U2FsdGVkX1-aXlqSUp"
    
    print(f"🔗 Исходный URL: {url}")
    
    # Кодируем URL
    encoded_url = urllib.parse.quote(url, safe='')
    proxy_url = f"http://localhost:8000/audio-proxy?url={encoded_url}"
    
    print(f"🔗 Прокси URL: {proxy_url[:100]}...")
    
    try:
        print("📡 Отправляю запрос...")
        response = requests.get(proxy_url, timeout=30)
        
        print(f"📊 Статус: {response.status_code}")
        print(f"📦 Размер: {len(response.content)} байт")
        print(f"🎵 Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("✅ Успех!")
            with open('/tmp/final_proxy_test.mp3', 'wb') as f:
                f.write(response.content)
            print("💾 Сохранено в /tmp/final_proxy_test.mp3")
            
            # Проверяем файл
            import os
            size = os.path.getsize('/tmp/final_proxy_test.mp3')
            print(f"📁 Размер файла: {size} байт")
            
        else:
            print(f"❌ Ошибка: {response.content[:500]}")
            
    except Exception as e:
        print(f"❌ Исключение: {str(e)}")

if __name__ == "__main__":
    test_proxy_final() 