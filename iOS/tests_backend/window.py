import pytest

from toga_iOS.libs import UIApplication, UIWindow

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, UIWindow)

    async def wait_for_window(self, message, minimize=False, full_screen=False):
        await self.redraw(message)

    @property
    def content_size(self):
        # Content height doesn't include the status bar or navigation bar.
        return (
            self.native.contentView.frame.size.width,
            self.native.contentView.frame.size.height
            - (
                UIApplication.sharedApplication.statusBarFrame.size.height
                + self.native.rootViewController.navigationBar.frame.size.height
            ),
        )

    async def close_info_dialog(self, dialog):
        self.native.rootViewController.dismissViewControllerAnimated(
            False, completion=None
        )
        dialog.native.actions[0].handler(dialog.native)
        await self.redraw("Info dialog dismissed")

    async def close_question_dialog(self, dialog, result):
        self.native.rootViewController.dismissViewControllerAnimated(
            False, completion=None
        )
        if result:
            dialog.native.actions[0].handler(dialog.native)
        else:
            dialog.native.actions[1].handler(dialog.native)
        await self.redraw(f"Question dialog ({'YES' if result else 'NO'}) dismissed")

    async def close_confirm_dialog(self, dialog, result):
        self.native.rootViewController.dismissViewControllerAnimated(
            False, completion=None
        )
        if result:
            dialog.native.actions[0].handler(dialog.native)
        else:
            dialog.native.actions[1].handler(dialog.native)
        await self.redraw(f"Question dialog ({'OK' if result else 'CANCEL'}) dismissed")

    async def close_error_dialog(self, dialog):
        self.native.rootViewController.dismissViewControllerAnimated(
            False, completion=None
        )
        dialog.native.actions[0].handler(dialog.native)
        await self.redraw("Error dialog dismissed")

    async def close_stack_trace_dialog(self, dialog, result):
        pytest.skip("Stack Trace dialog not implemented on iOS")

    async def close_save_file_dialog(self, dialog, result):
        pytest.skip("Save File dialog not implemented on iOS")

    async def close_open_file_dialog(self, dialog, result, multiple_select):
        pytest.skip("Open File dialog not implemented on iOS")

    async def close_select_folder_dialog(self, dialog, result, multiple_select):
        pytest.skip("Select Folder dialog not implemented on iOS")

    def has_toolbar(self):
        pytest.skip("Toolbars not implemented on iOS")
