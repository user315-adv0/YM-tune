from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import requests

class SimpleProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/proxy?'):
            # Парсим URL из параметра
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            url = params.get('url', [None])[0]
            
            if not url:
                self.send_error(400, "Missing URL parameter")
                return
            
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
                
                print(f"🔗 Запрос к: {url}")
                response = requests.get(url, stream=True, timeout=30, headers=headers)
                print(f"📡 Статус: {response.status_code}")
                print(f"📦 Размер: {len(response.content)} байт")
                print(f"🎵 Content-Type: {response.headers.get('content-type')}")
                
                if response.status_code not in [200, 206]:
                    self.send_error(response.status_code, "Audio file not found")
                    return
                
                # Отправляем заголовки
                self.send_response(200)
                self.send_header('Content-Type', response.headers.get('content-type', 'audio/mpeg'))
                self.send_header('Content-Length', str(len(response.content)))
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
                
                # Отправляем данные
                self.wfile.write(response.content)
                
            except Exception as e:
                print(f"❌ Ошибка: {str(e)}")
                self.send_error(500, f"Error: {str(e)}")
        else:
            self.send_error(404, "Not found")

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8001), SimpleProxyHandler)
    print("🚀 Простой прокси сервер запущен на http://localhost:8001")
    print("📝 Использование: http://localhost:8001/proxy?url=YOUR_URL")
    server.serve_forever() 