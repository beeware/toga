import os
from configparser import ConfigParser
from pathlib import Path

from toga import App


def _xdg_user_dir(name, fallback):
    """Resolve the location of an XDG user directory.

    Locations follow the freedesktop ``xdg-user-dirs`` tool: the
    ``user-dirs.dirs`` configuration file is consulted first, then the
    matching environment variable, then a default folder name in the user's
    home folder. This is the same resolution order used by ``platformdirs``.

    :param name: The xdg-user-dirs key for the folder (e.g. ``XDG_DESKTOP_DIR``).
    :param fallback: The name of the fallback folder in the user's home folder.
    """
    # The location of the user-dirs.dirs configuration file honors the XDG
    # base directory specification.
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
