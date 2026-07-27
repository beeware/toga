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

    def get_documents_path(self):
        raise RuntimeError("The web backend does not provide a user documents path")

    def get_pictures_path(self):
        raise RuntimeError("The web backend does not provide a user pictures path")

    def get_desktop_path(self):
        raise RuntimeError("The web backend does not provide a user desktop path")
