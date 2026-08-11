import os
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
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                base_dir = Path(local_app_data)
                if not base_dir.is_absolute():
                    base_dir = Path.home() / "AppData/Local"
            else:
                base_dir = Path.home() / "AppData/Local"
            return base_dir / author / App.app.formal_name

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

    def _xdg_path(env_var, default_path):
        value = os.environ.get(env_var)
        if value:
            path = Path(value)
            if path.is_absolute():
                return path
        return Path.home() / default_path

    class Paths:
        def __init__(self, interface):
            self.interface = interface

        def get_config_path(self):
            return _xdg_path("XDG_CONFIG_HOME", ".config") / App.app.app_name

        def get_data_path(self):
            return _xdg_path("XDG_DATA_HOME", ".local/share") / App.app.app_name

        def get_cache_path(self):
            return _xdg_path("XDG_CACHE_HOME", ".cache") / App.app.app_name

        def get_logs_path(self):
            return (
                _xdg_path("XDG_STATE_HOME", ".local/state") / App.app.app_name / "log"
            )
