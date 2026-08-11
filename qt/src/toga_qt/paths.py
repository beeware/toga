import os
from pathlib import Path

from toga import App


def _xdg_path(env_var, default_path):
    value = os.environ.get(env_var)
    if value:
        path = Path(value)
        if path.is_absolute():
            return path
    return Path.home() / default_path


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return _xdg_path("XDG_CONFIG_HOME", ".config") / App.app.app_name

    def get_data_path(self):
        return _xdg_path("XDG_DATA_HOME", ".local/share") / App.app.app_name

    def get_cache_path(self):
        return _xdg_path("XDG_CACHE_HOME", ".cache") / App.app.app_name

    def get_logs_path(self):
        return _xdg_path("XDG_STATE_HOME", ".local/state") / App.app.app_name / "log"
