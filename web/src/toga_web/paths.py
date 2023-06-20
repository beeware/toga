from pathlib import Path


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / "config"

    def get_data_path(self):
        return Path.home() / "data"

    def get_cache_path(self):
        return Path.home() / "cache"

    def get_logs_path(self):
        return Path.home() / "log"
