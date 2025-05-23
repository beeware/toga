import os
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def _get_root(self, envvar, default):
        custom_root = os.getenv(envvar)
        return Path(custom_root) if custom_root else Path.home() / default

    def get_config_path(self):
        root = self._get_root("XDG_CONFIG_HOME", ".config")
        return root / App.app.app_name

    def get_data_path(self):
        root = self._get_root("XDG_DATA_HOME", ".local/share")
        return root / App.app.app_name

    def get_cache_path(self):
        root = self._get_root("XDG_CACHE_HOME", ".cache")
        return root / App.app.app_name

    def get_logs_path(self):
        root = self._get_root("XDG_STATE_HOME", ".local/state")
        return root / App.app.app_name / "log"
