import requests

def test_proxy():
    url = "https://api.music.yandex.net/get-mp3/1ad2744c3318774cb5a4910112c81a7f/1981227b04f/U2FsdGVkX18ftC8UNn93on8pnGDcHGag-tSentd6dbL_F65pM_P61B5RytRr3cp_xQpDpYjlUdMLgmrK4oJeN1hRNvRQo0wpLBfcAhNzo1H-LRnows4ijXk4MV86L2WACdktumxLo7jzhl5F6hmgF_FFJfnWAhYKDYS0CZ4kZrKRk7Ff-1LK0JZQ1O71xH_iYykJWgNYv0tDstxfG26tt51HBPZz_F2bZfE2iRE8oMXYIoGUvcm9yTryisa42a5bpAqocyoxFJe_iCWPr-5ln_PzuE7gImnHRb7i2wKcEswI3CPrPgoQmYfqyJpBRNwLFPBTs9OmFJFxEBNTSm5sEObhL4q0O37fiw_aLYgKt1Z48nxMoAvM706Tr9I1VV1A_F4v4p7kNjMbtD1hQPUvz-T1BUfh50ZNTXy8e7kYfH9dTbsb9mbqUjrJdi4TtpndX4tpKTBbW8txDsoouONtzVFT0SdOOIPGsHMm3z4swLuGbM1p2UF3koorpiQ8-Loxoj5nyvnxh707b7igq_3ddX--BexFQQEn-JAqfX3De7OF4d6BqlkaKRiHF7Ymr2CDtTsPTSDO59lrDM1kZVv6UcfomQ0TDLB7FrlgHtiIgoYwwIcpS1isBYMZscZD9KNWRmkR4gNP7soHrtBkRp1NC0WQgvWWDx91sC0HKHHHUPQnuYDNoulMfnOoYWafVOIwbuFAT6aPaw7hEH8ODWZGQqoWb29QRZ6dwgh3ij0TTpUwthoTsqIRotY0TKckii9dF20iJB2AQWDYVZx4D64M6WtJraw3nLwiHVLABzwovGEqGex_IY5jZLWrsW1t2D5Bnci01nC7MC6TDQBi-98B7gwoaqOy5J-CAELuy3Vu2SMUTtVdVaXiEvfCzfkQO6CD7ocfzAgY8G-Yhgb0GTtCHv0lmrcmgoFsNOzrU7gY8tCE-Zdxjlfzb66kVK69eMYpTvhB4DCqy-IHfyESHnfyPA/-JzTrv8JbgegFe4X_JJobHoTQd7706CYH1petS25LIg"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
        'Accept-Encoding': 'identity',
        'Range': 'bytes=0-',
        'Referer': 'https://music.yandex.ru/',
        'Origin': 'https://music.yandex.ru'
    }
    
    print("🔗 Запрос к:", url)
    response = requests.get(url, stream=True, timeout=30, headers=headers)
    print(f"📡 Статус: {response.status_code}")
    print(f"📦 Размер: {len(response.content) if not response.headers.get('content-length') else response.headers.get('content-length')} байт")
    print(f"🎵 Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code not in [200, 206]:
        print(f"❌ Ошибка: {response.content[:500]}")
        return
    
    content_length = response.headers.get('content-length')
    if content_length and int(content_length) < 1000:
        print(f"⚠️ Подозрительно маленький файл: {content_length} байт")
        print(f"📄 Первые 200 байт: {response.content[:200]}")
        print(f"📄 Первые 200 байт (hex): {response.content[:200].hex()}")
    else:
        print("✅ Файл выглядит нормально")
        
        # Сохраняем первые 1KB для анализа
        with open('/tmp/test_audio.mp3', 'wb') as f:
            f.write(response.content[:1024])
        print("💾 Сохранено в /tmp/test_audio.mp3")

if __name__ == "__main__":
    test_proxy() 