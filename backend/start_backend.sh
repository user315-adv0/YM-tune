#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Запускаю backend..."
pkill -9 -f uvicorn || true
sleep 1

uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
PID=$!

# Ждем старта
for i in {1..10}; do
  sleep 1
  STATUS=$(curl -s http://localhost:8000/health || true)
  if [[ "$STATUS" == *"ok"* ]]; then
    echo "✅ Backend успешно запущен!"
    exit 0
  fi
done

echo "❌ Backend не стартовал. Проверь логи (ошибка импорта, порт занят, зависимость не установлена и т.д.)"
kill $PID
exit 1 