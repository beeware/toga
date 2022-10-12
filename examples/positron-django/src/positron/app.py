import os
import sys
import socketserver
from threading import Thread, Event
from wsgiref.simple_server import WSGIServer

import django
from django.core.servers.basehttp import WSGIRequestHandler
from django.core.handlers.wsgi import WSGIHandler

import toga


class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    pass


class Positron(toga.App):
    def web_server(self):
        # Use port 0 to let the server select an available port.
        self._httpd = ThreadedWSGIServer(("127.0.0.1", 0), WSGIRequestHandler)
        self._httpd.daemon_threads = True

        os.environ["DJANGO_SETTINGS_MODULE"] = "webapp.settings"
        django.setup(set_prefix=False)
        wsgi_handler = WSGIHandler()
        self._httpd.set_app(wsgi_handler)

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
