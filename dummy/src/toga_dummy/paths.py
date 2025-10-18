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
