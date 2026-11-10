from toga import App
from toga.paths import PlatformDirsPaths


class Paths(PlatformDirsPaths):
    def platformdirs_args(self):
        return {
            "appname": App.app.formal_name,
            "appauthor": "Unknown" if App.app.author is None else App.app.author,
        }

    # platformdirs uses the same location for config and data on Windows;
    # subfolders keep every app path distinct, and preserve the locations
    # used before platformdirs was introduced.
    def get_config_path(self):
        return super().get_config_path() / "Config"

    def get_data_path(self):
        return super().get_data_path() / "Data"
