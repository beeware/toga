import sys
from pathlib import Path

from toga import App

if sys.platform == "darwin":

    class Paths:
        def __init__(self, interface):
            self.interface = interface

        def get_config_path(self):
            return Path.home() / "Library/Preferences" / App.app.app_id

        def get_data_path(self):
            return Path.home() / "Library/Application Support" / App.app.app_id

        def get_cache_path(self):
            return Path.home() / "Library/Caches" / App.app.app_id

        def get_logs_path(self):
            return Path.home() / "Library/Logs" / App.app.app_id

elif sys.platform == "win32":

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

else:

    class Paths:
        def __init__(self, interface):
            self.interface = interface

        def get_config_path(self):
            return Path.home() / ".config" / App.app.app_name

        def get_data_path(self):
            return Path.home() / ".local/share" / App.app.app_name

        def get_cache_path(self):
            return Path.home() / ".cache" / App.app.app_name

        def get_logs_path(self):
            return Path.home() / ".local/state" / App.app.app_name / "log"
