from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    @property
    def __context(self):
        return App.app._impl.native.getApplicationContext()

    def get_config_path(self):
        return Path(self.__context.getFilesDir().getPath()) / "config"

    def get_data_path(self):
        return Path(self.__context.getFilesDir().getPath()) / "data"

    def get_cache_path(self):
        return Path(self.__context.getCacheDir().getPath())

    def get_logs_path(self):
        return Path(self.__context.getFilesDir().getPath()) / "log"
