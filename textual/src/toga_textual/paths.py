import sys
from functools import cached_property
from pathlib import Path

from toga import App

if sys.platform == "darwin":

    class Paths:
        def __init__(self, interface):
            self.interface = interface

        def get_config_path(self):
            return Path.home() / f"Library/Preferences/{App.app.app_id}"

        def get_data_path(self):
            return Path.home() / f"Library/Application Support/{App.app.app_id}"

        def get_cache_path(self):
            return Path.home() / f"Library/Caches/{App.app.app_id}"

        def get_logs_path(self):
            return Path.home() / f"Library/Logs/{App.app.app_id}"

elif sys.platform == "win32":

    class Paths:
        def __init__(self, interface):
            self.interface = interface

        @cached_property
        def _app_dir(self):
            # No coverage testing of this because we can't easily configure
            # the app to have no author.
            author = "Unknown" if App.app.author is None else App.app.author
            return Path.home() / f"AppData/Local/{author}/{App.app.formal_name}"

        # The rest are cached at the interface level:

        def get_config_path(self):
            return self._app_dir / "Config"

        def get_data_path(self):
            return self._app_dir / "Data"

        def get_cache_path(self):
            return self._app_dir / "Cache"

        def get_logs_path(self):
            return self._app_dir / "Logs"

else:

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
