from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    @property
    def author(self):
        if App.app.author is None:
            return "Toga"
        return App.app.author

    def get_config_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / self.author
            / App.app.formal_name
            / "Config"
        )

    def get_data_path(self):
        return Path.home() / "AppData" / "Local" / self.author / App.app.formal_name

    def get_cache_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / self.author
            / App.app.formal_name
            / "Cache"
        )

    def get_logs_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / self.author
            / App.app.formal_name
            / "Logs"
        )
