from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

def get_local_ip():
    """Получает локальный IP-адрес компьютера"""
    try:
        # Создаём временное соединение, чтобы узнать IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Все запросы отдают index.html
        self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        # Красивый вывод запросов в консоль
        print(f"  📱 {args[0]}")

PORT = 8000
LOCAL_IP = get_local_ip()

print('=' * 65)
print(f'✅ СЕРВЕР ЗАПУЩЕН!')
print('')
print(f'📌 НА КОМПЬЮТЕРЕ (этот ноутбук):')
print(f'   http://localhost:{PORT}')
print('')
print(f'📱 НА ТЕЛЕФОНЕ / ПЛАНШЕТЕ / ДРУГОМ КОМПЬЮТЕРЕ:')
print(f'   http://{LOCAL_IP}:{PORT}')
print('')
print('=' * 65)

# Запускаем сервер на всех интерфейсах (чтобы был доступ с телефона)
server = HTTPServer(('0.0.0.0', PORT), Handler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print('')
    print('🛑 Сервер остановлен')
    server.server_close()