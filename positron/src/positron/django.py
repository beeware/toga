from __future__ import annotations

from pathlib import Path

from briefcase.bootstraps import TogaGuiBootstrap


class DjangoPositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "does not support Web deployment"

    def app_source(self):
        return """\
import os
import socketserver
from threading import Event, Thread
from wsgiref.simple_server import WSGIServer

import django
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIRequestHandler

import toga


class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    pass


class {{ cookiecutter.class_name }}(toga.App):
    def web_server(self):
        print("Starting server...")
        # Use port 0 to let the server select an available port.
        self._httpd = ThreadedWSGIServer(("127.0.0.1", 0), WSGIRequestHandler)
        self._httpd.daemon_threads = True

        os.environ["DJANGO_SETTINGS_MODULE"] = "{{ cookiecutter.module_name }}.settings"
        django.setup(set_prefix=False)
        wsgi_handler = WSGIHandler()
        self._httpd.set_app(wsgi_handler)

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
        self.web_view.url = f"http://{{host}}:{{port}}/"

        self.main_window = toga.MainWindow()
        self.main_window.content = self.web_view
        self.main_window.show()


def main():
    return {{{{ cookiecutter.class_name }}}}()
"""

    def pyproject_table_briefcase_app_extra_content(self):
        return """
requires = [
    "django~=5.0",
]
test_requires = [
{% if cookiecutter.test_framework == "pytest" %}
    "pytest",
{% endif %}
]
"""

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        # settings.py
        (app_path / "settings.py").write_text(
            """
# TODO
""",
            encoding="UTF-8",
        )

        # urls.py
        (app_path / "urls.py").write_text(
            """\
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
""",
            encoding="UTF-8",
        )
