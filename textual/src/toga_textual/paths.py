import sys

from toga import App
from toga.paths import PlatformDirsPaths


class SubfolderPaths(PlatformDirsPaths):
    # platformdirs uses the same location for config and data on macOS and
    # Windows; subfolders keep every app path distinct.
    def get_config_path(self):
        return super().get_config_path() / "Config"

    def get_data_path(self):
        return super().get_data_path() / "Data"


if sys.platform == "darwin":

    class Paths(SubfolderPaths):
        def platformdirs_args(self):
            # macOS keys app-specific folders by bundle identifier.
            return {"appname": App.app.app_id}

elif sys.platform == "win32":

    class Paths(SubfolderPaths):
        def platformdirs_args(self):
            return {
                "appname": App.app.formal_name,
                "appauthor": "Unknown" if App.app.author is None else App.app.author,
            }

else:
    Paths = PlatformDirsPaths
