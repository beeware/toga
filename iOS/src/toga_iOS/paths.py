from pathlib import Path


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / "Library" / "Application support" / "Config"

    def get_data_path(self):
        return Path.home() / "Documents"

    def get_cache_path(self):
        return Path.home() / "Library" / "Caches"

    def get_logs_path(self):
        return Path.home() / "Library" / "Application support" / "Logs"
