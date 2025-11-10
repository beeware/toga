from functools import cached_property
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    @cached_property
    def _context(self):
        return App.app._impl.native.getApplicationContext()

    # The rest are cached at the interface level:

    def get_config_path(self):
        return Path(self._context.getFilesDir().getPath()) / "config"

    def get_data_path(self):
        return Path(self._context.getFilesDir().getPath()) / "data"

    def get_cache_path(self):
        return Path(self._context.getCacheDir().getPath())

    def get_logs_path(self):
        return Path(self._context.getFilesDir().getPath()) / "log"
