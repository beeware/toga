from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / "config" / App.app.app_id

    def get_data_path(self):
        return Path.home() / "user_data" / App.app.app_id

    def get_cache_path(self):
        return Path.home() / "cache" / App.app.app_id

    def get_logs_path(self):
        return Path.home() / "logs" / App.app.app_id

    def get_documents_path(self):
        return Path.home() / "Documents"

    def get_pictures_path(self):
        return Path.home() / "Pictures"

    def get_desktop_path(self):
        return Path.home() / "Desktop"
