# 🎵 Auto DJ - Автоматический DJ с кроссфейдом

MVP авто-DJ система с кроссфейдом, BPM-анализом и структурными переходами на базе Яндекс.Музыки.

## ✅ Что сделано

### Backend (Python + FastAPI)
- **Универсальный API** `/tracks/{id}` — поддерживает любые ID из Яндекс.Музыки
- **Поддержка источников:**
  - Альбомы (числовые ID: `7935690`)
  - Плейлисты (числовые ID: `123456`)
  - Любимые треки (`liked`)
  - Персональные плейлисты (`lk.xxx`)
- **Прямые ссылки** на mp3 файлы для скачивания
- **CORS настроен** для фронтенда
- **Обработка ошибок** и недоступных треков

### Frontend (React + TypeScript + Web Audio API)
- **Современный UI** с градиентами и анимациями
- **DJ плеер** с кроссфейдом (1-15 секунд)
- **Автоопределение типа** источника по ID
- **Список треков** с прогрессом воспроизведения
- **Адаптивный дизайн** для мобильных
- **Web Audio API** для качественного звука

### Функции
- ✅ **Кроссфейд** между треками без пауз
- ✅ **Автоматические переходы** с настраиваемой длительностью
- ✅ **Прямые URL** треков из Яндекс.Музыки
- ✅ **Универсальный ввод** — любой ID из Яндекс.Музыки
- ✅ **Современный UI** с индикаторами статуса
- ✅ **Обработка ошибок** и недоступных треков

## 🚀 Быстрый старт

### 1. Настройка токена Яндекс.Музыки

1. Откройте [music.yandex.ru](https://music.yandex.ru)
2. Войдите в свой аккаунт
3. Откройте DevTools (F12) → Console
4. Выполните: `yaMusic.getUser()`
5. Скопируйте значение `token`
6. Создайте файл `backend/.env`:
```env
YA_TOKEN=ваш_токен_здесь
```

### 2. Запуск

```bash
# Автоматический запуск (backend + frontend)
./start.sh

# Или вручную:
cd backend && pip install -r requirements.txt && uvicorn main:app --reload
cd frontend && npm install && npm run dev
```

### 3. Использование

1. Откройте http://localhost:5173
2. Введите ID источника:
   - `liked` — любимые треки
   - `7935690` — альбом (числовой ID)
   - `lk.xxx` — персональный плейлист
3. Настройте длительность кроссфейда (1-15 сек)
4. Нажмите "▶️ Запустить DJ"

## 🧪 Что тестить

### Рабочие источники:
- **Альбомы:** `7935690` (mgk - Sex Drive)
- **Любимые треки:** `liked` (если есть в аккаунте)
- **Плейлисты:** любые числовые ID

### Тестовые скрипты:
```bash
# Тест API
python test_api.py

# Тест любимых треков
python test_liked.py

# Тест универсального endpoint
python test_universal.py
```

### API Endpoints:
- `GET /` — статус API
- `GET /health` — проверка подключения к Яндекс.Музыке
- `GET /tracks/{id}` — универсальный endpoint
- `GET /playlist/{id}` — плейлисты
- `GET /liked` — любимые треки

## 🏗️ Архитектура

```
YA_API/
├── backend/                # Python + FastAPI
│   ├── main.py            # API сервер с универсальными endpoints
│   ├── yandex_client.py   # Клиент Яндекс.Музыки с поддержкой всех типов
│   ├── models.py          # Pydantic модели
│   ├── config.py          # Конфигурация и токен
│   └── requirements.txt   # Python зависимости
├── frontend/              # TypeScript + React + Vite
│   ├── src/
│   │   ├── App.tsx        # Основной UI с универсальным вводом
│   │   ├── api.ts         # API клиент с fetchTracks()
│   │   ├── player.ts      # DJ плеер с кроссфейдом
│   │   └── App.css        # Современные стили
│   ├── package.json       # Node зависимости
│   └── index.html         # HTML шаблон
├── start.sh               # Автозапуск
├── test_*.py              # Тестовые скрипты
└── README.md              # Документация
```

## 📝 TODO / Следующие шаги

### Приоритет 1 (MVP улучшения):
- [ ] **BPM анализ** треков для плавных переходов
- [ ] **Сортировка по BPM** (±3 BPM для гармоничных переходов
- [ ] **Определение onsets** (ключевых моментов) для точных переходов
- [ ] **Pitch-shift** для гармоничных переходов между разными тональностями

### Приоритет 2 (UI/UX):
- [ ] **Визуализация BPM** в списке треков
- [ ] **График кроссфейда** в реальном времени
- [ ] **Сохранение настроек** пользователя
- [ ] **Темная тема**

### Приоритет 3 (Инфраструктура):
- [ ] **Docker контейнеризация** (backend + frontend)
- [ ] **Unit тесты** (Jest + pytest)
- [ ] **CI/CD pipeline**
- [ ] **Мониторинг** и логирование

### Приоритет 4 (Расширения):
- [ ] **Spotify интеграция** (через Web Playback SDK)
- [ ] **YouTube Music** поддержка
- [ ] **Локальные файлы** (mp3, flac)
- [ ] **Экспорт плейлистов** в другие сервисы

## 🛠️ Технологии

**Backend:**
- Python 3.10+
- FastAPI (веб-фреймворк)
- yandex-music (API клиент)
- uvicorn (ASGI сервер)

**Frontend:**
- TypeScript
- React 18 (UI библиотека)
- Vite (сборщик)
- Web Audio API (звук)
- Axios (HTTP клиент)

## 🔧 Разработка

### Установка зависимостей:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Запуск в режиме разработки:
```bash
# Backend (с автоперезагрузкой)
cd backend && uvicorn main:app --reload

# Frontend (с HMR)
cd frontend && npm run dev
```

### Тестирование:
```bash
# API тесты
python test_universal.py

# Frontend тесты (будущие)
cd frontend && npm test
```

## 📄 Лицензия

MIT License

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте токен в `backend/.env`
2. Запустите тестовые скрипты
3. Проверьте логи backend/frontend
4. Создайте issue с описанием проблемы 