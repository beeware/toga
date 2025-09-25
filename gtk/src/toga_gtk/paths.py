import os
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def _get_root(self, envvar, default):
        custom_root_raw = os.getenv(envvar)
        custom_root = Path(custom_root_raw) if custom_root_raw else None

        # The XDG Base Directory spec requires paths to be absolute
        if custom_root and custom_root.is_absolute():
            return custom_root

        return Path.home() / default

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
