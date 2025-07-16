from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import requests

app = FastAPI()

@app.get("/test-proxy")
async def test_proxy(url: str):
    try:
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
        
        if response.status_code != 200:
            print(f"❌ Ошибка: {response.content[:500]}")
            raise HTTPException(status_code=response.status_code, detail="Аудио файл не найден")
        
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) < 1000:
            print(f"⚠️ Подозрительно маленький файл: {content_length} байт")
            print(f"📄 Первые 200 байт: {response.content[:200]}")
            print(f"📄 Первые 200 байт (hex): {response.content[:200].hex()}")
        
        return StreamingResponse(
            response.iter_content(chunk_size=8192),
            media_type=response.headers.get("content-type", "audio/mpeg"),
            headers={
                "Content-Length": response.headers.get("content-length", ""),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=3600"
            }
        )
    except Exception as e:
        import traceback
        print(f"❌ Ошибка прокси: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки аудио: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 