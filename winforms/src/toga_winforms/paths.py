from functools import cached_property
from pathlib import Path

from System import Environment

from toga import App

from .libs.shell32 import FOLDERID_Downloads, get_known_folder_path


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

    # User-space folders are resolved by the operating system, so folder
    # redirection (e.g., by OneDrive) is honored.

    def get_desktop_path(self):
        return Path(
            Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory)
        )

    def get_documents_path(self):
        return Path(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments))

    def get_downloads_path(self):
        # The SpecialFolder enum doesn't include the Downloads folder; it can
        # only be obtained from the Win32 known folder API.
        return Path(get_known_folder_path(FOLDERID_Downloads))

    def get_pictures_path(self):
        return Path(Environment.GetFolderPath(Environment.SpecialFolder.MyPictures))
