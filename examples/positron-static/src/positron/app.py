from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Event, Thread

import toga


class HTTPHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(self.server.base_path / path[1:])


class LocalHTTPServer(ThreadingHTTPServer):
    def __init__(self, base_path, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        # Use port 0 to let the server select an available port.
        super().__init__(("127.0.0.1", 0), RequestHandlerClass)


class Positron(toga.App):
    def web_server(self):
        print("Starting server...")
        self._httpd = LocalHTTPServer(self.paths.app / "resources" / "webapp")
        # The server is now listening, but connections will block until
        # serve_forever is run.
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
        host, port = self._httpd.socket.getsockname()
        self.web_view.url = f"http://{host}:{port}/"

        self.main_window = toga.MainWindow()
        self.main_window.content = self.web_view
        self.main_window.show()


def main():
    return Positron()
