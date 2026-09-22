import os
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    @property
    def _root(self):
        # Test suites can redirect all generated paths with TOGA_DUMMY_HOME.
        try:
            return Path(os.environ["TOGA_DUMMY_HOME"])
        except KeyError:
            return Path.home() / "toga-dummy"

    def get_config_path(self):
        return self._root / f"config/{App.app.app_id}"

    def get_data_path(self):
        return self._root / f"user_data/{App.app.app_id}"

    def get_cache_path(self):
        return self._root / f"cache/{App.app.app_id}"

    def get_logs_path(self):
        return self._root / f"logs/{App.app.app_id}"

    def get_desktop_path(self):
        return self._root / "desktop"

    def get_documents_path(self):
        return self._root / "documents"

    def get_downloads_path(self):
        return self._root / "downloads"

    def get_pictures_path(self):
        return self._root / "pictures"
