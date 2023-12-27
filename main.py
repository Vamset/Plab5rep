import http.server
import socketserver
import os

ROOT = 'C:\\Users\\Connor\\PycharmProjects\\Plab5'  # Путь к корневой директории сервера

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = self.translate_path(self.path)
        if os.path.isdir(self.path):
            return self.list_directory(self.path)
        else:
            return super().do_GET()

    def translate_path(self, path):
        return os.path.join(ROOT, *path.split('/'))

    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "Not found")
            return None
        list.sort(key=lambda a: a.lower())
        resp = '<!DOCTYPE html>\n<html><head><title>Directory listing</title></head><body>\n'
        resp += '<h1>Directory listing</h1>\n'
        resp += '<ul>\n'
        for file in list:
            resp += f'<li><a href="{file}">{file}</a></li>\n'
        resp += '</ul>\n'
        resp += '</body></html>\n'
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(resp)))
        self.end_headers()
        self.wfile.write(resp.encode())

def run(server_class=socketserver.TCPServer, handler_class=MyHttpRequestHandler):
    PORT = 65432  # Порт для запуска сервера
    with server_class(("", PORT), handler_class) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()

if __name__ == "__main__":
    run()