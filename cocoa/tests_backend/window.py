from rubicon.objc import objc_id, send_message

from toga_cocoa.libs import NSWindow, NSWindowStyleMask

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    supports_closable = True
    supports_minimizable = True
    supports_move_while_hidden = True
    supports_unminimize = True
    supports_minimize = True
    supports_placement = True

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, NSWindow)

    async def wait_for_window(
        self,
        message,
        minimize=False,
        full_screen=False,
        state_switch_not_from_normal=False,
    ):
        await self.redraw(
            message,
            delay=(
                1.75
                if state_switch_not_from_normal
                else 0.75 if full_screen else 0.5 if minimize else 0.1
            ),
        )

    def close(self):
        self.native.performClose(None)

    @property
    def content_size(self):
        return (
            self.impl.container.native.frame.size.width,
            self.impl.container.native.frame.size.height,
        )

    @property
    def is_resizable(self):
        return bool(self.native.styleMask & NSWindowStyleMask.Resizable)

    @property
    def is_closable(self):
        return bool(self.native.styleMask & NSWindowStyleMask.Closable)

    @property
    def is_minimizable(self):
        return bool(self.native.styleMask & NSWindowStyleMask.Miniaturizable)

    @property
    def is_minimized(self):
        return bool(self.native.isMiniaturized)

    def minimize(self):
        self.native.performMiniaturize(None)

    def unminimize(self):
        self.native.deminiaturize(None)

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def has_toolbar(self):
        return self.native.toolbar is not None

    def assert_is_toolbar_separator(self, index, section=False):
        item = self.native.toolbar.items[index]
        assert str(item.itemIdentifier).startswith(
            f"Toolbar-{'Separator' if section else 'Group'}"
        )

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        item = self.native.toolbar.items[index]

        assert str(item.label) == label
        assert (None if item.toolTip is None else str(item.toolTip)) == tooltip
        assert (item.image is not None) == has_icon
        assert item.isEnabled() == enabled

    def press_toolbar_button(self, index):
        item = self.native.toolbar.items[index]
        send_message(
            item.target,
            item.action,
            item,
            restype=None,
            argtypes=[objc_id],
        )

    def _setup_alert_dialog_result(self, dialog, result, pre_close_test_method=None):
        # Install an overridden show method that invokes the original,
        # but then closes the open dialog.
        orig_show = dialog._impl.show

        def automated_show(host_window, future):
            orig_show(host_window, future)
            try:
                if pre_close_test_method:
                    pre_close_test_method(dialog)
            finally:
                try:
                    dialog._impl.host_window.endSheet(
                        dialog._impl.host_window.attachedSheet,
                        returnCode=result,
                    )
                except Exception as e:
                    # An error occurred closing the dialog; that means the dialog
                    # isn't what as expected, so record that in the future.
                    future.set_exception(e)

        dialog._impl.show = automated_show

    def _setup_file_dialog_result(self, dialog, result):
        # Closing a window modal file dialog is the same as alerts.
        self._setup_alert_dialog_result(dialog, result)
