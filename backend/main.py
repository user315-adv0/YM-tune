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
client = YandexMusicClient(os.getenv('YA_TOKEN'))

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    try:
        # Проверяем подключение к Яндекс.Музыке
        is_connected = client.test_connection()
        return {"status": "ok", "yandex_connected": is_connected}
    except Exception as e:
        return {"status": "error", "yandex_connected": False, "error": str(e)}

@app.get("/audio-proxy")
async def audio_proxy(url: str):
    """Прокси для mp3 файлов с правильными заголовками"""
    try:
        # Заголовки для имитации браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'identity',
            'Range': 'bytes=0-',
            'Referer': 'https://music.yandex.ru/',
            'Origin': 'https://music.yandex.ru',
            'Sec-Fetch-Dest': 'audio',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }
        
        print(f"🔗 Проксируем: {url[:50]}...")
        
        # Делаем запрос к Яндексу
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        
        print(f"📡 Статус ответа: {response.status_code}")
        print(f"📦 Размер ответа: {len(response.content)} байт")
        
        if response.status_code != 200 and response.status_code != 206:
            raise HTTPException(status_code=response.status_code, detail="Ошибка получения аудио")
        
        # Проверяем, что это не превью
        if len(response.content) < 1000:
            print(f"⚠️ Получен слишком маленький файл ({len(response.content)} байт), возможно превью")
        
        # Возвращаем поток с правильными заголовками
        return StreamingResponse(
            response.iter_content(chunk_size=8192),
            media_type="audio/mpeg",
            headers={
                "Content-Type": "audio/mpeg",
                "Accept-Ranges": "bytes",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Content-Length": str(len(response.content)),
            }
        )
        
    except Exception as e:
        print(f"❌ Ошибка прокси: {e}")
        raise HTTPException(status_code=500, detail="Ошибка проксирования аудио")

@app.get("/tracks/{source_id}")
async def get_tracks(source_id: str):
    """Универсальный endpoint для получения треков"""
    try:
        tracks = client.fetch_tracks_universal(source_id)
        if not tracks:
            raise HTTPException(status_code=404, detail="Источник не найден")
        
        print(f"🔍 Получено треков: {len(tracks)}")
        
        # Добавляем прокси URL для каждого трека
        for i, track in enumerate(tracks):
            if track.url:
                print(f"🎵 Трек {i+1}: {track.title}")
                print(f"   До: {track.url[:50]}...")
                track.url = f"/audio-proxy?url={track.url}"
                print(f"   После: {track.url[:50]}...")
                track.bpm = None
        
        result = [track.dict() for track in tracks]
        print(f"📤 Отправляем результат с {len(result)} треками")
        return result
    except Exception as e:
        print(f"Ошибка при получении треков: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id: str):
    """Получение треков плейлиста"""
    try:
        tracks = client.fetch_playlist_tracks(playlist_id)
        if not tracks:
            raise HTTPException(status_code=404, detail="Плейлист не найден")
        
        # Добавляем прокси URL для каждого трека
        for track in tracks:
            if track.url:
                track.url = f"/audio-proxy?url={track.url}"
                track.bpm = None
        
        return [track.dict() for track in tracks]
    except Exception as e:
        print(f"Ошибка при получении плейлиста: {e}")
        raise HTTPException(status_code=404, detail="Плейлист не найден")

@app.get("/liked")
async def get_liked_tracks():
    """Получение любимых треков"""
    try:
        tracks = client.fetch_liked_tracks()
        if not tracks:
            raise HTTPException(status_code=404, detail="Нет любимых треков")
        
        # Добавляем прокси URL для каждого трека
        for track in tracks:
            if track.url:
                track.url = f"/audio-proxy?url={track.url}"
                track.bpm = None
        
        return [track.dict() for track in tracks]
    except Exception as e:
        print(f"Ошибка при получении любимых треков: {e}")
        raise HTTPException(status_code=404, detail="Не удалось получить любимые треки")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 