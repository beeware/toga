from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / ".config" / App.app.app_name

    def get_data_path(self):
        return Path.home() / ".local/share" / App.app.app_name

    def get_cache_path(self):
        return Path.home() / ".cache" / App.app.app_name

    def get_logs_path(self):
        return Path.home() / ".local/state" / App.app.app_name / "log"
