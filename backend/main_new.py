from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from yandex_client import YandexMusicClient
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI(title="Auto DJ API")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация клиента Яндекс.Музыки
client = YandexMusicClient(os.getenv('YANDEX_TOKEN'))

@app.get("/audio-proxy")
async def audio_proxy(url: str):
    """Прокси для скачивания аудио файлов"""
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

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    try:
        # Проверяем подключение к Яндекс.Музыке
        is_connected = client.test_connection()
        return {"status": "ok", "yandex_connected": is_connected}
    except Exception as e:
        return {"status": "error", "yandex_connected": False, "error": str(e)}

@app.get("/tracks/{source_id}")
async def get_tracks(source_id: str):
    """Универсальный endpoint для получения треков"""
    try:
        tracks = client.fetch_tracks_universal(source_id)
        
        if not tracks:
            raise HTTPException(status_code=404, detail="Источник не найден")
        
        # Заменяем прямые URL на прокси URL
        for track in tracks:
            if track.url:
                # Временно убираем BPM-анализ
                track.bpm = None
                
                # Заменяем URL на прокси
                track.url = f"/audio-proxy?url={track.url}"
        
        return [track.dict() for track in tracks]
        
    except Exception as e:
        print(f"Ошибка при получении треков: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 