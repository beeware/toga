import os
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / f"config/{App.app.app_id}"

    def get_data_path(self):
        return Path.home() / f"user_data/{App.app.app_id}"

    def get_cache_path(self):
        return Path.home() / f"cache/{App.app.app_id}"

    def get_logs_path(self):
        return Path.home() / f"logs/{App.app.app_id}"

    def _user_dir(self, name):
        # User-space folders are returned as clearly dummy locations in the
        # user's home folder. A test suite can redirect them to a temporary
        # location by setting the TOGA_DUMMY_USER_DIRS environment variable,
        # ensuring tests can't accidentally touch a real permanent location.
        try:
            root = Path(os.environ["TOGA_DUMMY_USER_DIRS"])
        except KeyError:
            root = Path.home() / "toga-dummy"
        return root / name

    def get_desktop_path(self):
        return self._user_dir("desktop")

    def get_documents_path(self):
        return self._user_dir("documents")

    def get_downloads_path(self):
        return self._user_dir("downloads")

    def get_pictures_path(self):
        return self._user_dir("pictures")
