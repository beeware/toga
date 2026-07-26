from pathlib import Path

from toga import App

from .libs import GLib


def user_path(directory, default):
    return Path(GLib.get_user_special_dir(directory) or Path.home() / default)


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return Path.home() / f".config/{App.app.app_name}"

    def get_data_path(self):
        return Path.home() / f".local/share/{App.app.app_name}"

    def get_cache_path(self):
        return Path.home() / f".cache/{App.app.app_name}"

    def get_logs_path(self):
        return Path.home() / f".local/state/{App.app.app_name}/log"

    def get_documents_path(self):
        return user_path(GLib.UserDirectory.DIRECTORY_DOCUMENTS, "Documents")

    def get_pictures_path(self):
        return user_path(GLib.UserDirectory.DIRECTORY_PICTURES, "Pictures")

    def get_desktop_path(self):
        return user_path(GLib.UserDirectory.DIRECTORY_DESKTOP, "Desktop")
