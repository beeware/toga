from pathlib import Path

from toga_iOS.libs import (
    NSFileManager,
    NSSearchPathDirectory,
    NSSearchPathDomainMask,
    UIApplication,
)

from .probe import BaseProbe


class AppProbe(BaseProbe):
    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, UIApplication)

    def get_path(self, search_path):
        file_manager = NSFileManager.defaultManager
        urls = file_manager.URLsForDirectory(
            search_path, inDomains=NSSearchPathDomainMask.User
        )
        return Path(urls[0].path)

    @property
    def config_path(self):
        return self.get_path(NSSearchPathDirectory.ApplicationSupport) / "Config"

    @property
    def data_path(self):
        return self.get_path(NSSearchPathDirectory.Documents)

    @property
    def cache_path(self):
        return self.get_path(NSSearchPathDirectory.Cache)

    @property
    def logs_path(self):
        return self.get_path(NSSearchPathDirectory.ApplicationSupport) / "Logs"
