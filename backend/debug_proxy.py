import requests
import urllib.parse

def test_proxy():
    # URL из треков
    url = "https://api.music.yandex.net/get-mp3/2b34e4248106b3d4f538c0bdabcc398a/198123cc3c9/U2FsdGVkX18gOQHdctd0APONHhaADxKMeTro-j0rd2oap1mRRW4hKLGK3dxBxNByqw3attYv95S9b3mxIyIqcFRzkXsgEFisOpAO4KP7NYGXT1kWtro-9fWvk2k_lqtqzEQG02TjIOA0cLOS9EGVT1nW5EJMkdA2KXdl41okYIEdAz1KXF0QYa-aTfZhUNKFSPyJRAjOG7daWEWOt_9iYM1pMyyEQdV7bo9cBcOTeYMsnl22smGNkpW9KDQAC1hL3TZ0Ftt0SN0F126BmweFKY_MVjjOj_iK_Eiy5y9KpO3MztNd73tW7biyR-tjB1pxBfYUiQMBd4btUnjJSWVwXLEp3TSSk0v9edI7RK0W94JPfpZFRh5wfy-2OfYBA7xQjv74JYfFExB47WM8K4NnUddCdm2j7-SdtyuhLZYd75a7VGX2s1s6QDzk_x6fhFo8GoVhsIVLnJ2HFRm-lSVmTD2jCvKuo-W55UUmmIbQog8_-6T9SaqGo5dfWfDObs27ojt4wOpTiNSa7aegIgyHrM8j_0AhHHxiGZ0B-u_1qGKj0DzhkJ0svwr4Y6PSU2wjSKaU0dTZBh54X0M52Mw7D4vVxSNVdye2wjUGv6AhAGhOGGsVbhncsMDNi7jqv61Zv4Rsy3e-iGMGxHDrpsdAluGNmgPd48mS1VJ7asn9ufQtdr-MIt4Eh8gx-M_zg1gHPEhACZdfRhk8_H6WUUsN84QPJr0Gtf_05-qjl9C5B1nyAlFT4qVHsvuQoPOLX_prU1FkmrAY9IQ1_bICc6sg2KTDL9gWkxDZhQLLNPViAIJU-edUgTmmP9vm0vy5mA46hnT4BqafJyG9FOT6-kBWtsILQQEXPhbiNSeMkv8gUT_chPE7DdtudnXvYnNxfyjaG_0u-9DkXC-YXvCMZd-A_LK7tmVkF49oIPkWIauTjonPsd3agrHfcughwTJdW_MurtVUQZPx2X3f8U0q_Oha"
    
    print(f"🔗 Исходный URL: {url[:100]}...")
    print(f"📏 Длина URL: {len(url)}")
    
    # Кодируем URL для прокси
    encoded_url = urllib.parse.quote(url, safe='')
    proxy_url = f"http://localhost:8000/audio-proxy?url={encoded_url}"
    
    print(f"🔗 Прокси URL: {proxy_url[:100]}...")
    print(f"📏 Длина прокси URL: {len(proxy_url)}")
    
    try:
        print("📡 Отправляю запрос...")
        response = requests.get(proxy_url, timeout=30)
        
        print(f"📊 Статус: {response.status_code}")
        print(f"📦 Размер: {len(response.content)} байт")
        print(f"🎵 Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("✅ Успех!")
            with open('/tmp/debug_test.mp3', 'wb') as f:
                f.write(response.content)
            print("💾 Сохранено в /tmp/debug_test.mp3")
        else:
            print(f"❌ Ошибка: {response.content[:500]}")
            
    except Exception as e:
        print(f"❌ Исключение: {str(e)}")
        import traceback
        print(f"📋 Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_proxy() 