from toga import App
from toga.paths import PlatformDirsPaths


class Paths(PlatformDirsPaths):
    def platformdirs_args(self):
        # macOS keys app-specific folders by bundle identifier.
        return {"appname": App.app.app_id}

    # platformdirs uses the same location for config and data on macOS;
    # subfolders keep every app path distinct.
    def get_config_path(self):
        return super().get_config_path() / "Config"

    def get_data_path(self):
        return super().get_data_path() / "Data"
