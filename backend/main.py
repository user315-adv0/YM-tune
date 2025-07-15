from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Track
from yandex_client import YandexMusicClient
from config import YA_TOKEN

app = FastAPI(title="Auto DJ API", version="1.0.0")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализируем клиент
if not YA_TOKEN:
    print("❌ YA_TOKEN не настроен!")
    ya_client = None
else:
    ya_client = YandexMusicClient(YA_TOKEN)

@app.get("/")
async def root():
    return {"message": "Auto DJ API работает!", "token_configured": YA_TOKEN is not None}

@app.get("/health")
async def health_check():
    if not ya_client:
        raise HTTPException(status_code=500, detail="Токен Яндекс.Музыки не настроен")
    
    is_connected = ya_client.test_connection()
    return {"status": "ok", "yandex_connected": is_connected}

@app.get("/playlist/{playlist_id}", response_model=List[Track])
async def get_playlist(playlist_id: str):
    """Получает треки плейлиста с прямыми URL для скачивания"""
    if not ya_client:
        raise HTTPException(status_code=500, detail="Токен Яндекс.Музыки не настроен")
    
    tracks = ya_client.fetch_playlist_tracks(playlist_id)
    
    if not tracks:
        raise HTTPException(status_code=404, detail="Плейлист не найден или пуст")
    
    return tracks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 