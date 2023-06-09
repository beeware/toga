from pathlib import Path

from toga_iOS.libs import NSFileManager, NSSearchPathDirectory, NSSearchPathDomainMask


class Paths:
    def __init__(self, interface):
        self.interface = interface

    def get_path(self, search_path):
        file_manager = NSFileManager.defaultManager
        urls = file_manager.URLsForDirectory(
            search_path, inDomains=NSSearchPathDomainMask.User
        )
        return Path(urls[0].path)

    def get_config_path(self):
        return self.get_path(NSSearchPathDirectory.ApplicationSupport) / "Config"

    def get_data_path(self):
        return self.get_path(NSSearchPathDirectory.Documents)

    def get_cache_path(self):
        return self.get_path(NSSearchPathDirectory.Cache)

    def get_logs_path(self):
        return self.get_path(NSSearchPathDirectory.ApplicationSupport) / "Logs"
