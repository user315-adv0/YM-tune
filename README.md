# About

**YA Auto-DJ** — MVP автодиджея с кроссфейдом и BPM-анализом на базе Яндекс.Музыки.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

- Backend: Python + FastAPI (проксирует mp3, работает с OAuth-токеном Яндекс.Музыки, выбирает лучшее качество)
- Frontend: React + TypeScript (плеер с кроссфейдом, выбор качества)
- Особенности: прямые mp3-ссылки быстро устаревают, поэтому используется прокси с авторизацией
- Ограничения: Яндекс может отдавать только превью через прокси, CORS-блокировки, нестабильность mp3-URL

---

# Project structure

- backend/ — FastAPI backend, вся логика работы с Яндекс.Музыкой, прокси, OAuth
  - main.py — основной сервер
  - yandex_client.py — работа с API Яндекс.Музыки
  - config.py, models.py — конфиги и модели
- frontend/ — React + TypeScript SPA
  - src/ — исходники фронта (App.tsx, player.ts, api.ts)
- README.md — документация

---

# 🎵 Auto DJ - Автоматический DJ с кроссфейдом

Автоматический DJ плеер с кроссфейдом и BPM-анализом на базе Яндекс.Музыки.

## 🚀 Возможности

- **Автоматический кроссфейд** между треками
- **BPM-анализ** для синхронизации
- **Интеграция с Яндекс.Музыкой** через API
- **Современный React + TypeScript** интерфейс
- **FastAPI** backend с прокси для аудио
- **Выбор лучшего качества** (320kbps)

## 🏗️ Архитектура

```
YA_API/
├── backend/          # FastAPI сервер
│   ├── main.py      # Основной API
│   ├── yandex_client.py  # Клиент Яндекс.Музыки
│   └── models.py    # Pydantic модели
├── frontend/         # React + TypeScript
│   └── src/
│       ├── App.tsx  # Главный компонент
│       └── player.ts # DJ плеер с кроссфейдом
└── README.md
```

## 🛠️ Установка и запуск

### Backend (Python + FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

### Переменные окружения

Создайте `backend/.env`:
```env
YA_TOKEN=your_yandex_music_oauth_token
```

## 📊 Текущий статус

### ✅ Реализовано

- [x] **Backend API** с FastAPI
- [x] **Интеграция с Яндекс.Музыкой** через yandex-music
- [x] **Получение треков** из альбомов, плейлистов, "Мне нравятся"
- [x] **Выбор лучшего качества** (320kbps вместо 192kbps)
- [x] **Прокси для аудио** с CORS заголовками
- [x] **React фронтенд** с TypeScript
- [x] **DJ плеер** с автоматическим переключением
- [x] **Кроссфейд** между треками
- [x] **Отладочная информация** в консоли

### 🔧 Решённые проблемы

1. **CORS блокировка** - реализован прокси `/audio-proxy?url=...`
2. **Превью вместо полного mp3** - добавлены правильные заголовки браузера
3. **Выбор качества** - автоматический выбор 320kbps
4. **Ошибки авторизации** - исправлено имя переменной `YA_TOKEN`

### ⚠️ Текущие проблемы

1. **Размер аудио файлов** - прокси возвращает 639 байт вместо полного mp3
   - **Статус**: В работе
   - **Причина**: Яндекс возвращает превью несмотря на заголовки
   - **Решение**: Экспериментируем с дополнительными заголовками

2. **Ошибка "Unable to decode audio data"**
   - **Статус**: Связана с проблемой #1
   - **Причина**: Слишком маленький файл (639 байт)
   - **Решение**: Исправить получение полного mp3

### 🎯 Следующие шаги

1. **Исправить получение полного mp3** через прокси
2. **Добавить BPM-анализ** для синхронизации
3. **Улучшить кроссфейд** с плавными переходами
4. **Добавить визуализацию** аудио
5. **Оптимизировать производительность**

## 🔍 Отладка

### Backend логи

При запросе `/tracks/7935690` в консоли backend:
```
🔍 Получено треков: 14
🎵 Трек 1: Sex Drive
   До: https://api.music.yandex.net/get-mp3/...
   После: /audio-proxy?url=https://api.music.yandex.net/get-mp3/...
📤 Отправляем результат с 14 треками
```

### Frontend логи

В консоли браузера:
```
🔄 Загружаю аудио: /audio-proxy?url=https://api.music.yandex.net/get-mp3/...
📡 Ответ сервера: 200 OK
📦 Размер аудио данных: 639 байт
❌ Ошибка загрузки аудио: EncodingError: Unable to decode audio data
```

## 🧪 Тестирование

### Проверка backend

```bash
# Проверка здоровья API
curl http://localhost:8000/health

# Получение треков
curl http://localhost:8000/tracks/7935690

# Тест прокси
curl "http://localhost:8000/audio-proxy?url=YOUR_MP3_URL"
```

### Проверка frontend

1. Откройте http://localhost:5173
2. Нажмите "Start DJ"
3. Проверьте консоль браузера на ошибки

## 📝 Changelog

### v0.2.0 (Текущая версия)
- ✅ Добавлен прокси для обхода CORS
- ✅ Реализован выбор лучшего качества (320kbps)
- ✅ Добавлена отладочная информация
- ✅ Исправлена авторизация Яндекс.Музыки
- ⚠️ Проблема с размером аудио файлов (639 байт)

### v0.1.0
- ✅ Базовая интеграция с Яндекс.Музыкой
- ✅ React фронтенд с TypeScript
- ✅ DJ плеер с автоматическим переключением
- ❌ CORS ошибки при воспроизведении

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🔗 Ссылки

- [Яндекс.Музыка API](https://github.com/MarshalX/yandex-music-api)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/) 

## TODO

### 🔧 Технические улучшения
- [ ] Исправить проблему с получением полного mp3 через прокси (сейчас возвращается превью)
- [ ] Добавить BPM-анализ треков для автоматического кроссфейда
- [ ] Реализовать кэширование mp3-файлов для стабильности
- [ ] Добавить WebSocket для real-time обновлений плеера
- [ ] Оптимизировать прокси для обхода ограничений Яндекса

### 🎵 Функциональность
- [ ] Автоматический подбор треков по BPM
- [ ] Плейлисты и история воспроизведения
- [ ] Поиск по трекам и артистам
- [ ] Настройки качества звука
- [ ] Эквалайзер и эффекты

### 🚀 Продакшен
- [ ] Docker-контейнеризация
- [ ] CI/CD pipeline
- [ ] Мониторинг и логирование
- [ ] Rate limiting для API
- [ ] Тесты (unit, integration)

### 📱 UX/UI
- [ ] Адаптивный дизайн для мобильных
- [ ] Темная тема
- [ ] Анимации переходов
- [ ] Клавиатурные shortcuts
- [ ] Drag & drop для плейлистов 