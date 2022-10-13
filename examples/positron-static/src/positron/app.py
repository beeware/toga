from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread, Event

import toga


class HTTPHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(self.server.base_path / path[1:])


class LocalHTTPServer(HTTPServer):
    def __init__(self, base_path, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        # Use port 0 to let the server select an available port.
        super().__init__(("127.0.0.1", 0), RequestHandlerClass)


class Positron(toga.App):
    def web_server(self):
        print("Starting server...")
        self._httpd = LocalHTTPServer(self.paths.app / "resources" / "webapp")
        self.server_exists.set()
        self._httpd.serve_forever()

    def cleanup(self, app, **kwargs):
        print("Shutting down...")
        self._httpd.shutdown()
        return True

    def startup(self):
        self.server_exists = Event()

        self.web_view = toga.WebView()

        self.server_thread = Thread(target=self.web_server)
        self.server_thread.start()

        self.on_exit = self.cleanup

        self.server_exists.wait()
        # This will block until the server is active
        host, port = self._httpd.socket.getsockname()
        self.web_view.url = f'http://{host}:{port}/'

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.web_view
        self.main_window.show()


def main():
    return Positron()
