import os
import sys
from functools import cached_property
from pathlib import Path

from toga import App


def user_path(key, default):
    config_home = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    try:
        lines = (
            (config_home / "user-dirs.dirs").read_text(encoding="utf-8").splitlines()
        )
    except OSError:
        return Path.home() / default

    for line in lines:
        name, separator, value = line.partition("=")
        if name == key and separator:
            return Path(value.strip().strip('"').replace("$HOME", str(Path.home())))
    return Path.home() / default


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

        def get_documents_path(self):
            return Path.home() / "Documents"

        def get_pictures_path(self):
            return Path.home() / "Pictures"

        def get_desktop_path(self):
            return Path.home() / "Desktop"

elif sys.platform == "win32":
    from winreg import HKEY_CURRENT_USER, KEY_READ, OpenKey, QueryValueEx

    def _user_shell_folder(name, default):
        try:
            with OpenKey(
                HKEY_CURRENT_USER,
                "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer"
                "\\User Shell Folders",
                0,
                KEY_READ,
            ) as key:
                return QueryValueEx(key, name)[0]
        except OSError:
            return default

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

        def get_documents_path(self):
            return Path(
                os.path.expandvars(
                    _user_shell_folder("Personal", Path.home() / "Documents")
                )
            )

        def get_pictures_path(self):
            return Path(
                os.path.expandvars(
                    _user_shell_folder("My Pictures", Path.home() / "Pictures")
                )
            )

        def get_desktop_path(self):
            return Path(
                os.path.expandvars(
                    _user_shell_folder("Desktop", Path.home() / "Desktop")
                )
            )

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

        def get_documents_path(self):
            return user_path("XDG_DOCUMENTS_DIR", "Documents")

        def get_pictures_path(self):
            return user_path("XDG_PICTURES_DIR", "Pictures")

        def get_desktop_path(self):
            return user_path("XDG_DESKTOP_DIR", "Desktop")
