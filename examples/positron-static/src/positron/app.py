import sys
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
        print("Starting server...", file=sys.stderr)
        self._httpd = LocalHTTPServer(self.paths.app / "resources" / "webapp")
        self.is_serving.set()
        self._httpd.serve_forever()

    def cleanup(self, app, **kwargs):
        print("Shutting down...", file=sys.stderr)
        self._httpd.server_close()
        return True

    def wait_for_webserver(self):
        self.is_serving.wait()
        return self._httpd.socket.getsockname()

    def startup(self):
        self._httpd = None
        self.is_serving = Event()

        self.web_view = toga.WebView()

        self.server_thread = Thread(target=self.web_server)
        self.server_thread.start()

        self.on_exit = self.cleanup

        host, port = self.wait_for_webserver()
        self.web_view.url = f'http://{host}:{port}/'

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.web_view
        self.main_window.show()


def main():
    return Positron()
