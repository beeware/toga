from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / f"Library/Preferences/{App.app.app_id}"

    def get_data_path(self):
        return Path.home() / f"Library/Application Support/{App.app.app_id}"

    def get_cache_path(self):
        return Path.home() / f"Library/Caches/{App.app.app_id}"

    def get_logs_path(self):
        return Path.home() / f"Library/Logs/{App.app.app_id}"
