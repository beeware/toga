import os
from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return (
            Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
            / App.app.app_name
        )

    def get_data_path(self):
        return (
            Path(os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local/share"))
            / App.app.app_name
        )

    def get_cache_path(self):
        return (
            Path(os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache"))
            / App.app.app_name
        )

    def get_logs_path(self):
        return (
            Path(os.environ.get("XDG_STATE_HOME") or (Path.home() / ".local/state"))
            / App.app.app_name
            / "log"
        )
