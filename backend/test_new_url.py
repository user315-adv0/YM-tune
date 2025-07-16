import requests
import urllib.parse

def test_new_url():
    # НОВЫЙ URL из логов backend
    new_url = "https://api.music.yandex.net/get-mp3/fbad280aacb30f10bc7aaecb93d408b9/1981240b289/U2FsdGVkX18DeB2br2d9UZl2yQsOkbdUgxdUhqROQ2e42llTYFgLAgS4p7XZh3Y29ZujLy0PN4Flgb3VdHE815Y2KPGvulN71a0irttFU5F-x8izmXRAeA2e_o8WvNm-DFEkvTQ5oDJhI0v80xJ518IeUkxCUzH0acZfVzBt4rK4L11_W9-YX_UhGkntRiIJgaBwf1KEuaY23Se6bmcKdBDlzGknatOBsC-_tu-0HKdegMWKEZdqHZeuX-d89vsddjoV1XOx8fy0xuS9gkoLPLqTVDIWi_RsezsDv637xfImCT6VCSDqnQF7yp_Bmqblt7Sn7OtYG2kbikZvwtH0RD9IruxAm58Rt0xl2-lnR6xZ2JuYhu9Fz0yfdEVrlIw8HwnCuvmH5583IjODqOZaLMFh1cer9us8AS1ArcZr3EewgQJuUnOiRLJegFMMdVAuwCkr7nKSb-kOAk3J1ugoXFB_IAfA07hhLqnxIP7F95QqdBGC1-fZ64rTiQO-Pmjdip1YF5sv8cH4IFn5e2zsqujBCjQiHhcl_2z8f-Sdn1JSRdkJI_bB2_GU9nnPSBiYjfjY24Z0MAtfcB0WgA_Dm2tQJDJjWoBL_lyVkqZJzByLkKp9wIMfrBh72cKcMzNyHUsZX_VP40kKLS4c4o1ysk3MaBpHki3uWYG8d2oL7YjJ-eTxc3b7WmMU6FyrptubqEifIolQEYUYYq1Cw1W2MZg-j-UldjVWBXdB07yaRrXsfaapywc7_f4K5i2kOLwv95eoh"
    
    print(f"🔗 Новый URL: {new_url[:100]}...")
    print(f"📏 Длина URL: {len(new_url)}")
    
    # Кодируем URL для прокси
    encoded_url = urllib.parse.quote(new_url, safe='')
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
            with open('/tmp/new_url_test.mp3', 'wb') as f:
                f.write(response.content)
            print("💾 Сохранено в /tmp/new_url_test.mp3")
            
            # Проверяем файл
            import os
            size = os.path.getsize('/tmp/new_url_test.mp3')
            print(f"📁 Размер файла: {size} байт")
            
        else:
            print(f"❌ Ошибка: {response.content[:500]}")
            
    except Exception as e:
        print(f"❌ Исключение: {str(e)}")

if __name__ == "__main__":
    test_new_url() 