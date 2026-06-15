from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

state = "off"


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global state

        if self.path == "/on":
            state = "on"
        elif self.path == "/off":
            state = "off"

        background = "#2ecc71" if state == "on" else "#e74c3c"

        html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{state.upper()}</title>
    <style>
        body {{
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background: {background};
            font-family: Arial, sans-serif;
        }}

        .status {{
            font-size: 25vw;
            font-weight: 900;
            color: white;
            text-shadow: 0 10px 30px rgba(0,0,0,0.2);
            letter-spacing: 10px;
        }}
    </style>
</head>
<body>
    <div class="status">{state.upper()}</div>
</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"Запрос: {self.path}")


PORT = 8000
LOCAL_IP = get_local_ip()

print("=" * 65)
print("СЕРВЕР ЗАПУЩЕН")
print(f"На компьютере: http://localhost:{PORT}")
print(f"На телефоне: http://{LOCAL_IP}:{PORT}")
print("")
print("Команды:")
print(f"Включить:  http://localhost:{PORT}/on")
print(f"Выключить: http://localhost:{PORT}/off")
print("=" * 65)

server = HTTPServer(("0.0.0.0", PORT), Handler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Сервер остановлен")
    server.server_close()
