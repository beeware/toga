from __future__ import annotations

from pathlib import Path

from briefcase.bootstraps import TogaGuiBootstrap


class StaticPositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    def app_source(self):
        return """\
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


class {{ cookiecutter.class_name }}(toga.App):
    def web_server(self):
        print("Starting server...")
        self._httpd = LocalHTTPServer(self.paths.app / "resources")
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
    return {{ cookiecutter.class_name }}()
"""

    def post_generate(self, base_path: Path):
        resource_path = base_path / "src" / self.context["module_name"] / "resources"

        # Write an index.html file
        (resource_path / "index.html").write_text(
            f"""<html>
    <head>
        <title>{self.context["formal_name"]}</title>
        <link rel="stylesheet" href="./positron.css" type="text/css">
    </head>
    <body>
        <h1>Hello World</h1>
    </body>
</html>
""",
            encoding="UTF-8",
        )

        # Write a CSS file
        (resource_path / "positron.css").write_text(
            """
h1 {
    font-family: sans-serif;
}
""",
            encoding="UTF-8",
        )
