# 🎵 Auto DJ - Автоматический DJ с кроссфейдом

MVP авто-DJ система с кроссфейдом, BPM-анализом и структурными переходами на базе Яндекс.Музыки.

## 🚀 Быстрый старт

### 1. Настройка токена Яндекс.Музыки

1. Откройте DevTools в браузере на music.yandex.ru
2. В консоли выполните: `yaMusic.getUser()`
3. Скопируйте токен и создайте файл `backend/.env`:
```env
YA_TOKEN=ваш_токен_здесь
```

### 2. Запуск Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Запуск Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Использование

1. Откройте http://localhost:5173
2. Введите ID плейлиста Яндекс.Музыки
3. Настройте длительность кроссфейда
4. Нажмите "Запустить DJ"

## 🏗️ Архитектура

```
YA_API/
├── backend/                # Python + FastAPI
│   ├── main.py            # API сервер
│   ├── yandex_client.py   # Клиент Яндекс.Музыки
│   ├── models.py          # Pydantic модели
│   ├── config.py          # Конфигурация
│   └── requirements.txt   # Python зависимости
└── frontend/              # TypeScript + React + Vite
    ├── src/
    │   ├── App.tsx        # Основной UI
    │   ├── api.ts         # API клиент
    │   ├── player.ts      # DJ плеер с кроссфейдом
    │   └── App.css        # Стили
    ├── package.json       # Node зависимости
    └── index.html         # HTML шаблон
```

## 🎛️ Функции

- ✅ **Кроссфейд** между треками (1-15 сек)
- ✅ **Автоматические переходы** без пауз
- ✅ **Web Audio API** для качественного воспроизведения
- ✅ **Прямые URL** треков из Яндекс.Музыки
- ✅ **Современный UI** с прогресс-баром
- ✅ **Адаптивный дизайн** для мобильных

## 🔧 API Endpoints

- `GET /` - Статус API
- `GET /health` - Проверка подключения к Яндекс.Музыке
- `GET /playlist/{id}` - Получение треков плейлиста

## 📝 TODO

- [ ] BPM анализ треков
- [ ] Сортировка по BPM для плавных переходов
- [ ] Определение ключевых моментов (onsets)
- [ ] Pitch-shift для гармоничных переходов
- [ ] Сохранение настроек пользователя
- [ ] Docker контейнеризация

## 🛠️ Технологии

**Backend:**
- Python 3.10+
- FastAPI
- yandex-music
- uvicorn

**Frontend:**
- TypeScript
- React 18
- Vite
- Web Audio API
- Axios

## 📄 Лицензия

MIT License 