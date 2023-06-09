from pathlib import Path

from toga import App


class Paths:
    def __init__(self, interface):
        self.interface = interface

    @property
    def author(self):
        # No coverage testing of this because we can't easily configure
        # the app to have no author.
        if App.app.author is None:  # pragma: no cover
            return "Unknown"
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
        return (
            Path.home()
            / "AppData"
            / "Local"
            / self.author
            / App.app.formal_name
            / "Data"
        )

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
