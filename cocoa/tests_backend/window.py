from unittest.mock import Mock

from rubicon.objc import objc_id, send_message
from rubicon.objc.collections import ObjCListInstance

from toga_cocoa.libs import (
    NSURL,
    NSAlertFirstButtonReturn,
    NSAlertSecondButtonReturn,
    NSModalResponseCancel,
    NSModalResponseOK,
    NSOpenPanel,
    NSSavePanel,
    NSWindow,
    NSWindowStyleMask,
)

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    supports_closable = True
    supports_minimizable = True
    supports_move_while_hidden = True
    supports_multiple_select_folder = True
    supports_unminimize = True

    def __init__(self, app, window):
        super().__init__()
        self.app = app
        self.window = window
        self.impl = window._impl
        self.native = window._impl.native
        assert isinstance(self.native, NSWindow)

    async def wait_for_window(self, message, minimize=False, full_screen=False):
        await self.redraw(
            message,
            delay=0.75 if full_screen else 0.5 if minimize else 0.1,
        )

    def close(self):
        self.native.performClose(None)

    @property
    def content_size(self):
        return (
            self.native.contentView.frame.size.width,
            self.native.contentView.frame.size.height,
        )

    @property
    def is_full_screen(self):
        return bool(self.native.styleMask & NSWindowStyleMask.FullScreen)

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

    async def close_info_dialog(self, dialog):
        self.native.endSheet(
            self.native.attachedSheet,
            returnCode=NSAlertFirstButtonReturn,
        )
        await self.redraw("Info dialog dismissed")

    async def close_question_dialog(self, dialog, result):
        if result:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSAlertFirstButtonReturn,
            )
        else:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSAlertSecondButtonReturn,
            )
        await self.redraw(f"Question dialog ({'YES' if result else 'NO'}) dismissed")

    async def close_confirm_dialog(self, dialog, result):
        if result:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSAlertFirstButtonReturn,
            )
        else:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSAlertSecondButtonReturn,
            )

        await self.redraw(f"Question dialog ({'OK' if result else 'CANCEL'}) dismissed")

    async def close_error_dialog(self, dialog):
        self.native.endSheet(
            self.native.attachedSheet,
            returnCode=NSAlertFirstButtonReturn,
        )
        await self.redraw("Error dialog dismissed")

    async def close_stack_trace_dialog(self, dialog, result):
        if result is None:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSAlertFirstButtonReturn,
            )
            await self.redraw("Stack trace dialog dismissed")
        else:
            if result:
                self.native.endSheet(
                    self.native.attachedSheet,
                    returnCode=NSAlertFirstButtonReturn,
                )
            else:
                self.native.endSheet(
                    self.native.attachedSheet,
                    returnCode=NSAlertSecondButtonReturn,
                )

            await self.redraw(
                f"Stack trace dialog ({'RETRY' if result else 'QUIT'}) dismissed"
            )

    async def close_save_file_dialog(self, dialog, result):
        assert isinstance(dialog.native, NSSavePanel)

        if result:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSModalResponseOK,
            )
        else:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSModalResponseCancel,
            )

        await self.redraw(
            f"Save file dialog ({'SAVE' if result else 'CANCEL'}) dismissed"
        )

    async def close_open_file_dialog(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, NSOpenPanel)

        if result is not None:
            if multiple_select:
                # Since we are mocking selected_path(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(dialog.selected_paths(), ObjCListInstance)

                dialog.selected_paths = Mock(
                    return_value=[
                        NSURL.fileURLWithPath(str(path), isDirectory=False)
                        for path in result
                    ]
                )
            else:
                dialog.selected_path = Mock(
                    return_value=NSURL.fileURLWithPath(
                        str(result),
                        isDirectory=False,
                    )
                )

            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSModalResponseOK,
            )
        else:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSModalResponseCancel,
            )

        await self.redraw(
            f"Open {'multiselect ' if multiple_select else ''}file dialog "
            f"({'OPEN' if result else 'CANCEL'}) dismissed"
        )

    async def close_select_folder_dialog(self, dialog, result, multiple_select):
        assert isinstance(dialog.native, NSOpenPanel)

        if result is not None:
            if multiple_select:
                # Since we are mocking selected_path(), it's never actually invoked
                # under test conditions. Call it just to confirm that it returns the
                # type we think it does.
                assert isinstance(dialog.selected_paths(), ObjCListInstance)

                dialog.selected_paths = Mock(
                    return_value=[
                        NSURL.fileURLWithPath(str(path), isDirectory=True)
                        for path in result
                    ]
                )
            else:
                dialog.selected_path = Mock(
                    return_value=NSURL.fileURLWithPath(
                        str(result),
                        isDirectory=True,
                    )
                )

            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSModalResponseOK,
            )
        else:
            self.native.endSheet(
                self.native.attachedSheet,
                returnCode=NSModalResponseCancel,
            )

        await self.redraw(
            f"{'Multiselect' if multiple_select else ' Select'} folder dialog "
            f"({'OPEN' if result else 'CANCEL'}) dismissed"
        )

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
