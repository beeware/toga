from pathlib import Path

from PySide6.QtCore import QStandardPaths

from toga import App


def app_path(location, default):
    return Path(QStandardPaths.writableLocation(location) or default) / App.app.app_name


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_config_path(self):
        return app_path(
            QStandardPaths.StandardLocation.GenericConfigLocation,
            Path.home() / ".config",
        )

    def get_data_path(self):
        return app_path(
            QStandardPaths.StandardLocation.GenericDataLocation,
            Path.home() / ".local/share",
        )

    def get_cache_path(self):
        return app_path(
            QStandardPaths.StandardLocation.GenericCacheLocation,
            Path.home() / ".cache",
        )

    def get_logs_path(self):
        return (
            app_path(
                QStandardPaths.StandardLocation.GenericStateLocation,
                Path.home() / ".local/state",
            )
            / "log"
        )

    def get_documents_path(self):
        return Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
            or Path.home() / "Documents"
        )

    def get_pictures_path(self):
        return Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.PicturesLocation
            )
            or Path.home() / "Pictures"
        )

    def get_desktop_path(self):
        return Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DesktopLocation
            )
            or Path.home() / "Desktop"
        )
