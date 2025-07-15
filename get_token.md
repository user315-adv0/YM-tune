# 🔑 Как получить токен Яндекс.Музыки

## Способ 1: Через DevTools (Рекомендуется)

1. Откройте [music.yandex.ru](https://music.yandex.ru)
2. Войдите в свой аккаунт
3. Откройте DevTools (F12 или Ctrl+Shift+I)
4. Перейдите на вкладку Console
5. Выполните команду:
```javascript
yaMusic.getUser()
```
6. Скопируйте значение `token` из ответа
7. Создайте файл `backend/.env` и добавьте:
```env
YA_TOKEN=ваш_токен_здесь
```

## Способ 2: Через Network Tab

1. Откройте DevTools → Network
2. Обновите страницу music.yandex.ru
3. Найдите запрос к API (например, `/handlers/...`)
4. В заголовках запроса найдите `Authorization: OAuth ваш_токен`
5. Скопируйте токен и добавьте в `.env`

## Проверка токена

После настройки запустите backend и проверьте:
```bash
curl http://localhost:8000/health
```

Должен вернуться: `{"status": "ok", "yandex_connected": true}` 