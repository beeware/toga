from contextlib import contextmanager
from pathlib import Path

import pytest

from toga_iOS.libs import (
    NSFileManager,
    NSSearchPathDirectory,
    NSSearchPathDomainMask,
    UIApplication,
)

from .dialogs import DialogsMixin
from .probe import BaseProbe


class AppProbe(BaseProbe, DialogsMixin):
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

    @contextmanager
    def prepare_paths(self, *, custom):
        if custom:
            pytest.xfail("This backend doesn't implement app path customization.")

        yield {
            "config": self.get_path(NSSearchPathDirectory.ApplicationSupport)
            / "Config",
            "data": self.get_path(NSSearchPathDirectory.Documents),
            "cache": self.get_path(NSSearchPathDirectory.Cache),
            "logs": self.get_path(NSSearchPathDirectory.ApplicationSupport) / "Logs",
        }

    def assert_app_icon(self, icon):
        pytest.xfail("iOS apps don't have app icons at runtime")

    def assert_dialog_in_focus(self, dialog):
        root_view_controller = self.native.keyWindow.rootViewController
        assert (
            root_view_controller.presentedViewController == dialog._impl.native
        ), "The dialog is not in focus"

    def assert_system_menus(self):
        pytest.skip("Menus not implemented on iOS")

    def activate_menu_about(self):
        pytest.skip("Menus not implemented on iOS")

    def activate_menu_visit_homepage(self):
        pytest.skip("Menus not implemented on iOS")

    def assert_menu_item(self, path, enabled):
        pytest.skip("Menus not implemented on iOS")

    def assert_menu_order(self, path, expected):
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

    def has_status_icon(self, status_icon):
        pytest.xfail("Status icons not implemented on iOS")

    def status_menu_items(self, status_icon):
        pytest.xfail("Status icons not implemented on iOS")

    def activate_status_icon_button(self, item_id):
        pytest.xfail("Status icons not implemented on iOS")

    def activate_status_menu_item(self, item_id, title):
        pytest.xfail("Status icons not implemented on iOS")
