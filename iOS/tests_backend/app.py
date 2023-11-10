from pathlib import Path

import pytest

from toga_iOS.libs import (
    NSFileManager,
    NSSearchPathDirectory,
    NSSearchPathDomainMask,
    UIApplication,
)

from .probe import BaseProbe


class AppProbe(BaseProbe):
    supports_key = False

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.native = self.app._impl.native
        assert isinstance(self.native, UIApplication)

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

    def assert_system_menus(self):
        pytest.skip("Menus not implemented on iOS")

    def activate_menu_about(self):
        pytest.skip("Menus not implemented on iOS")

    def activate_menu_visit_homepage(self):
        pytest.skip("Menus not implemented on iOS")

    def assert_menu_item(self, path, enabled):
        pytest.skip("Menus not implemented on iOS")

    def enter_background(self):
        self.native.delegate.applicationWillResignActive(self.native)
        self.native.delegate.applicationDidEnterBackground(self.native)

    def enter_foreground(self):
        self.native.delegate.applicationWillEnterForeground(self.native)

    def terminate(self):
        self.native.delegate.applicationWillTerminate(self.native)

    def rotate(self):
        self.native = self.app._impl.native
        self.native.delegate.application(self.native, didChangeStatusBarOrientation=0)
