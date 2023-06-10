from pathlib import Path

from toga_cocoa.libs import NSApplication

from .probe import BaseProbe


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, NSApplication)

    @property
    def config_path(self):
        return Path.home() / "Library" / "Preferences" / "org.beeware.toga.testbed"

    @property
    def data_path(self):
        return (
            Path.home() / "Library" / "Application Support" / "org.beeware.toga.testbed"
        )

    @property
    def cache_path(self):
        return Path.home() / "Library" / "Caches" / "org.beeware.toga.testbed"

    @property
    def logs_path(self):
        return Path.home() / "Library" / "Logs" / "org.beeware.toga.testbed"
