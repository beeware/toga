from functools import cached_property
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    @cached_property
    def _app_dir(self):
        # No coverage testing of this because we can't easily configure
        # the app to have no author.
        author = "Unknown" if App.app.author is None else App.app.author
        return Path.home() / f"AppData/Local/{author}/{App.app.formal_name}"

    # The rest are cached at the interface level:

    def get_config_path(self):
        return self._app_dir / "Config"

    def get_data_path(self):
        return self._app_dir / "Data"

    def get_cache_path(self):
        return self._app_dir / "Cache"

    def get_logs_path(self):
        return self._app_dir / "Logs"
