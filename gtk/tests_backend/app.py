from pathlib import Path

from toga_gtk.libs import Gtk

from .probe import BaseProbe


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, Gtk.Application)

    @property
    def config_path(self):
        return Path.home() / ".config" / "testbed"

    @property
    def data_path(self):
        return Path.home() / ".local" / "share" / "testbed"

    @property
    def cache_path(self):
        return Path.home() / ".cache" / "testbed"

    @property
    def logs_path(self):
        return Path.home() / ".local" / "state" / "testbed" / "log"
