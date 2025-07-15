#!/bin/bash

echo "🎵 Запуск Auto DJ..."

# Проверяем наличие .env файла
if [ ! -f "backend/.env" ]; then
    echo "❌ Файл backend/.env не найден!"
    echo "📝 Создайте файл backend/.env с YA_TOKEN=ваш_токен"
    echo "📖 Смотрите get_token.md для инструкций"
    exit 1
fi

# Запускаем backend
echo "🚀 Запуск backend..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Ждем запуска backend
sleep 3

# Запускаем frontend
echo "🎨 Запуск frontend..."
cd frontend
npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Auto DJ запущен!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Ожидаем прерывания
trap "echo '🛑 Остановка...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 