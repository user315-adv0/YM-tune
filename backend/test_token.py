from yandex_music import Client
import os
from dotenv import load_dotenv

load_dotenv()

def test_token():
    token = os.getenv('YA_TOKEN')
    print(f"🔑 Токен: {token[:20]}...")
    
    try:
        # Инициализируем клиент
        client = Client(token).init()
        print("✅ Клиент инициализирован")
        
        # Проверяем статус аккаунта
        account = client.account_status()
        print(f"✅ Аккаунт: {account.account.login}")
        print(f"✅ Имя: {account.account.full_name}")
        print(f"✅ Премиум: {getattr(account.account, 'premium', 'N/A')}")
        
        # Получаем треки альбома
        album = client.albums_with_tracks("7935690")
        if album and album.volumes:
            track = album.volumes[0][0]  # Первый трек
            print(f"🎵 Трек: {track.title}")
            
            # Получаем информацию для скачивания
            download_info = track.get_download_info()
            if download_info:
                print(f"📥 Доступно качеств: {len(download_info)}")
                for i, info in enumerate(download_info):
                    print(f"  {i}: {info.bitrate_in_kbps}kbps, {info.codec}")
                
                # Получаем прямую ссылку
                direct_link = download_info[0].get_direct_link()
                print(f"🔗 Прямая ссылка: {direct_link[:100]}...")
                
                # Проверяем, работает ли ссылка
                import requests
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Authorization': f'OAuth {token}',
                    'Cookie': f'YandexMusic=OAuth {token}'
                }
                
                response = requests.head(direct_link, headers=headers, timeout=10, allow_redirects=True)
                print(f"📡 Статус прямой ссылки: {response.status_code}")
                print(f"📦 Content-Length: {response.headers.get('content-length')}")
                
            else:
                print("❌ Нет информации для скачивания")
        else:
            print("❌ Альбом не найден")
            
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_token() 