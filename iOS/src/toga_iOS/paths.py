from pathlib import Path


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_paths(self):
        return Path.home() / "Library" / "Application support" / "Config"

    def get_data_paths(self):
        return Path.home() / "Documents"

    def get_cache_paths(self):
        return Path.home() / "Library" / "Caches"

    def get_logs_paths(self):
        return Path.home() / "Library" / "Application support" / "Logs"
