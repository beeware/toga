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

    # Web apps can't access the user's file system.

    def get_desktop_path(self):
        raise RuntimeError("Web apps cannot access the user's Desktop folder")

    def get_documents_path(self):
        raise RuntimeError("Web apps cannot access the user's Documents folder")

    def get_downloads_path(self):
        raise RuntimeError("Web apps cannot access the user's Downloads folder")

    def get_pictures_path(self):
        raise RuntimeError("Web apps cannot access the user's Pictures folder")
