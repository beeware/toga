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

        # User-space folder names are fixed on macOS (localization is only
        # applied when the folder names are *displayed*).

        def get_desktop_path(self):
            return Path.home() / "Desktop"

        def get_documents_path(self):
            return Path.home() / "Documents"

        def get_downloads_path(self):
            return Path.home() / "Downloads"

        def get_pictures_path(self):
            return Path.home() / "Pictures"

elif sys.platform == "win32":
    from ctypes import HRESULT, POINTER, byref, c_char_p, c_wchar_p, windll, wintypes
    from uuid import UUID

    # https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid
    FOLDERID_Desktop = UUID("{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}")
    FOLDERID_Documents = UUID("{FDD39AD0-238F-46AF-ADB4-6C85480369C7}")
    FOLDERID_Downloads = UUID("{374DE290-123F-4565-9164-39C4925E467B}")
    FOLDERID_Pictures = UUID("{33E28130-4E1E-4676-835A-98395C3BC3BB}")

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.restype = HRESULT
    SHGetKnownFolderPath.argtypes = [
        c_char_p,  # REFKNOWNFOLDERID rfid (pointer to 16 byte GUID data)
        wintypes.DWORD,  # DWORD dwFlags
        wintypes.HANDLE,  # HANDLE hToken
        POINTER(c_wchar_p),  # PWSTR *ppszPath
    ]

    CoTaskMemFree = windll.ole32.CoTaskMemFree
    CoTaskMemFree.restype = None
    CoTaskMemFree.argtypes = [c_wchar_p]

    def _known_folder_path(folder_id):
        """Return the current path of a Windows known folder, so folder
        redirection (e.g., by OneDrive) is honored."""
        path_ptr = c_wchar_p()
        # The HRESULT restype raises OSError if the call fails.
        SHGetKnownFolderPath(folder_id.bytes_le, 0, None, byref(path_ptr))
        try:
            return Path(path_ptr.value)
        finally:
            CoTaskMemFree(path_ptr)

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

        def get_desktop_path(self):
            return _known_folder_path(FOLDERID_Desktop)

        def get_documents_path(self):
            return _known_folder_path(FOLDERID_Documents)

        def get_downloads_path(self):
            return _known_folder_path(FOLDERID_Downloads)

        def get_pictures_path(self):
            return _known_folder_path(FOLDERID_Pictures)

else:
    import os
    from configparser import ConfigParser

    def _xdg_user_dir(name, fallback):
        """Resolve the location of an XDG user directory.

        Locations follow the freedesktop ``xdg-user-dirs`` tool: the
        ``user-dirs.dirs`` configuration file is consulted first, then the
        matching environment variable, then a default folder name in the
        user's home folder. This is the same resolution order used by
        ``platformdirs``.

        :param name: The xdg-user-dirs key for the folder (e.g.
            ``XDG_DESKTOP_DIR``).
        :param fallback: The name of the fallback folder in the user's home
            folder.
        """
        # The location of the user-dirs.dirs configuration file honors the
        # XDG base directory specification.
        config_file = (
            Path(os.environ.get("XDG_CONFIG_HOME") or "~/.config").expanduser()
            / "user-dirs.dirs"
        )
        if config_file.exists():
            # The file is a sequence of shell-style NAME="$HOME/folder" lines;
            # parse it by injecting a section header, as platformdirs does.
            parser = ConfigParser(interpolation=None)
            parser.read_string("[user-dirs]\n" + config_file.read_text())
            try:
                path = parser["user-dirs"][name]
            except KeyError:
                pass
            else:
                return Path(path.strip('"').replace("$HOME", str(Path.home())))

        try:
            return Path(os.environ[name])
        except KeyError:
            return Path.home() / fallback

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

        def get_desktop_path(self):
            return _xdg_user_dir("XDG_DESKTOP_DIR", "Desktop")

        def get_documents_path(self):
            return _xdg_user_dir("XDG_DOCUMENTS_DIR", "Documents")

        def get_downloads_path(self):
            return _xdg_user_dir("XDG_DOWNLOAD_DIR", "Downloads")

        def get_pictures_path(self):
            return _xdg_user_dir("XDG_PICTURES_DIR", "Pictures")
