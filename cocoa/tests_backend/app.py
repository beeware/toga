from pathlib import Path

import PIL.Image
from rubicon.objc import SEL, NSPoint, ObjCClass, objc_id, send_message

import toga
from toga_cocoa.keys import cocoa_key, toga_key
from toga_cocoa.libs import (
    NSApplication,
    NSEvent,
    NSEventModifierFlagShift,
    NSEventType,
    NSWindow,
)

from .dialogs import DialogsMixin
from .probe import BaseProbe, NSRunLoop

NSPanel = ObjCClass("NSPanel")
NSDate = ObjCClass("NSDate")


class AppProbe(BaseProbe, DialogsMixin):
    supports_key = True
    supports_key_mod3 = True
    supports_current_window_assignment = True

    def __init__(self, app):
        super().__init__()
        self.app = app

        # Prevents erroneous test fails from secondary windows opening as tabs
        NSWindow.allowsAutomaticWindowTabbing = False
        assert isinstance(self.app._impl.native, NSApplication)

    @property
    def config_path(self):
        return Path.home() / "Library/Preferences/org.beeware.toga.testbed"

    @property
    def data_path(self):
        return Path.home() / "Library/Application Support/org.beeware.toga.testbed"

    @property
    def cache_path(self):
        return Path.home() / "Library/Caches/org.beeware.toga.testbed"

    @property
    def logs_path(self):
        return Path.home() / "Library/Logs/org.beeware.toga.testbed"

    @property
    def is_cursor_visible(self):
        # There's no API level mechanism to detect cursor visibility;
        # fall back to the implementation's proxy variable.
        return self.app._impl._cursor_visible

    def is_full_screen(self, window):
        return window._impl.container.native.isInFullScreenMode()

    def content_size(self, window):
        return (
            window.content._impl.native.frame.size.width,
            window.content._impl.native.frame.size.height,
        )

    def assert_app_icon(self, icon):
        # We have no real way to check we've got the right icon; use pixel peeping as a
        # guess. Construct a PIL image from the current icon.
        img = toga.Image(
            NSApplication.sharedApplication.applicationIconImage
        ).as_format(PIL.Image.Image)

        # Due to icon resizing and colorspace issues, the exact pixel colors are
        # inconsistent, so multiple values must be provided for test purposes.
        if icon:
            # The explicit alt icon has blue background, with green at a point 1/3 into
            # the image
            assert img.getpixel((5, 5)) in {
                (205, 226, 243, 255),
                (211, 226, 243, 255),
                (211, 230, 245, 255),
            }
            mid_color = img.getpixel((img.size[0] // 3, img.size[1] // 3))
            assert mid_color in {
                (0, 204, 9, 255),
                (6, 204, 8, 255),
                (14, 197, 8, 255),
                (105, 192, 32, 255),
            }
        else:
            # The default icon is transparent background, and brown in the center.
            assert img.getpixel((5, 5))[3] == 0
            mid_color = img.getpixel((img.size[0] // 2, img.size[1] // 2))
            assert mid_color in {
                (130, 100, 57, 255),
                (130, 109, 66, 255),
                (138, 107, 64, 255),
                (138, 108, 64, 255),
                (149, 119, 73, 255),
            }

    def _menu_item(self, path):
        main_menu = self.app._impl.native.mainMenu

        menu = main_menu
        orig_path = path.copy()
        while True:
            label, path = path[0], path[1:]
            item = menu.itemWithTitle(label)
            if item is None:
                raise AssertionError(
                    f"Menu {' > '.join(orig_path)} not found; "
                    f"no item named {label!r}; options are: "
                    + ",".join(f"{str(item.title)!r}" for item in menu.itemArray)
                )

            if path:
                menu = item.submenu
                if menu is None:
                    raise AssertionError(
                        f"Menu {' > '.join(orig_path)} not found; "
                        f"{str(item.title)} does not have a submenu"
                    )
            else:
                # No more path segments; we've found the full path.
                break

        return item

    def _activate_menu_item(self, path):
        item = self._menu_item(path)
        send_message(
            self.app._impl.native.delegate,
            item.action,
            item,
            restype=None,
            argtypes=[objc_id],
        )

    def activate_menu_exit(self):
        self._activate_menu_item(["*", "Quit Toga Testbed"])

    def activate_menu_about(self):
        self._activate_menu_item(["*", "About Toga Testbed"])

    async def close_about_dialog(self):
        about_dialog = self.app._impl.native.keyWindow
        if isinstance(about_dialog, NSPanel):
            about_dialog.close()

    def activate_menu_visit_homepage(self):
        self._activate_menu_item(["Help", "Visit homepage"])

    def assert_system_menus(self):
        self.assert_menu_item(["*", "About Toga Testbed"], enabled=True)
        self.assert_menu_item(["*", "Hide Toga Testbed"], enabled=True)
        self.assert_menu_item(["*", "Hide Others"], enabled=True)
        self.assert_menu_item(["*", "Show All"], enabled=True)
        self.assert_menu_item(["*", "Quit Toga Testbed"], enabled=True)

        self.assert_menu_item(["File", "New Example Document"], enabled=True)
        self.assert_menu_item(["File", "New Read-only Document"], enabled=True)
        self.assert_menu_item(["File", "Open\u2026"], enabled=True)
        self.assert_menu_item(["File", "Save"], enabled=True)
        self.assert_menu_item(["File", "Save As\u2026"], enabled=True)
        self.assert_menu_item(["File", "Save All"], enabled=True)
        self.assert_menu_item(["File", "Close"], enabled=True)
        self.assert_menu_item(["File", "Close All"], enabled=True)

        self.assert_menu_item(["Edit", "Undo"], enabled=True)
        self.assert_menu_item(["Edit", "Redo"], enabled=True)
        self.assert_menu_item(["Edit", "Cut"], enabled=True)
        self.assert_menu_item(["Edit", "Copy"], enabled=True)
        self.assert_menu_item(["Edit", "Paste"], enabled=True)
        self.assert_menu_item(["Edit", "Paste and Match Style"], enabled=True)
        self.assert_menu_item(["Edit", "Delete"], enabled=True)
        self.assert_menu_item(["Edit", "Select All"], enabled=True)

        self.assert_menu_item(["Window", "Minimize"], enabled=True)

        self.assert_menu_item(["Help", "Visit homepage"], enabled=True)

    def activate_menu_close_window(self):
        self._activate_menu_item(["File", "Close"])

    def activate_menu_close_all_windows(self):
        self._activate_menu_item(["File", "Close All"])

    def activate_menu_minimize(self):
        self._activate_menu_item(["Window", "Minimize"])

    def assert_menu_item(self, path, enabled):
        item = self._menu_item(path)
        assert item.isEnabled() == enabled

    def assert_menu_order(self, path, expected):
        menu = self._menu_item(path).submenu

        assert menu.numberOfItems == len(expected)
        for item, title in zip(menu.itemArray, expected):
            if title == "---":
                assert item.isSeparatorItem
            else:
                assert item.title == title

    def keystroke(self, combination):
        key, modifiers = cocoa_key(combination)
        key_code = {
            "a": 0,
            "A": 0,
            "1": 18,
            "!": 18,
            "'": 39,
            ";": 41,
            "|": 42,
            " ": 49,
            chr(0xF708): 96,  # F5
            chr(0xF729): 115,  # Home
            # This only works because we're *not* testing the numeric 5
            "5": 87,
        }[key]

        # Add the shift modifier to disambiguate shifted keys from non-shifted
        if key in {"!", "|"}:
            modifiers |= NSEventModifierFlagShift

        event = NSEvent.keyEventWithType(
            NSEventType.KeyDown,
            location=NSPoint(0, 0),  # key presses don't have a location.
            modifierFlags=modifiers,
            timestamp=0,
            windowNumber=self.app.main_window._impl.native.windowNumber,
            context=None,
            characters="?",
            charactersIgnoringModifiers="?",
            isARepeat=False,
            keyCode=key_code,
        )
        return toga_key(event)

    async def restore_standard_app(self):
        # If the tesbed app has been made a background app, it will no longer be
        # active, which affects whether it can receive focus and input events.
        # Make it active again. This won't happen immediately; allow for a short
        # delay.
        self.app._impl.native.activateIgnoringOtherApps(True)
        await self.redraw("Restore to standard app", delay=0.1)

    def _setup_alert_dialog_result(self, dialog, result):
        # Replace the dialog polling mechanism with an implementation that polls
        # 5 times, then returns the required result.
        _poll_modal_session = dialog._impl._poll_modal_session
        count = 0

        def auto_poll_modal_session(nsapp, session):
            nonlocal count
            if count < 5:
                count += 1
                return _poll_modal_session(nsapp, session)
            return result

        dialog._impl._poll_modal_session = auto_poll_modal_session

    def _setup_file_dialog_result(self, dialog, result):
        # Install an overridden show method that invokes the original,
        # but then closes the open dialog.
        orig_show = dialog._impl.show

        def automated_show(host_window, future):
            orig_show(host_window, future)

            # Inject a small pause without blocking the event loop
            NSRunLoop.currentRunLoop.runUntilDate(
                NSDate.dateWithTimeIntervalSinceNow(1.0 if self.app.run_slow else 0.2)
            )
            # Close the dialog and trigger the completion handler
            dialog._impl.native.close()
            dialog._impl.completion_handler(result)

        dialog._impl.show = automated_show

    async def open_initial_document(self, monkeypatch, document_path):
        # Mock the async menu item with an implementation that directly opens the doc
        async def _mock_open():
            self.app.documents.open(document_path)

        monkeypatch.setattr(self.app.documents, "request_open", _mock_open)

        # Call the APIs that are triggered when the app is activated.
        nsapp = self.app._impl.native

        # We are running in an async context. Invoking a selector moves
        # to an sync context, but the handling needs to queue an async
        # task. By invoking the relevant methods using Objective C's
        # deferred invocation mechanism, the method is invoked in a
        # sync context, so it is able to queue the required async task.
        nsapp.delegate.performSelector(
            SEL("applicationShouldOpenUntitledFile:"),
            withObject=nsapp,
            afterDelay=0.01,
        )
        nsapp.delegate.performSelector(
            SEL("applicationOpenUntitledFile:"),
            withObject=nsapp,
            afterDelay=0.02,
        )

        await self.redraw("Initial document has been triggered", delay=0.1)

    def open_document_by_drag(self, document_path):
        self.app._impl.native.delegate.application(
            self.app._impl.native,
            openFiles=[str(document_path)],
        )

    def has_status_icon(self, status_icon):
        return status_icon._impl.native is not None

    def status_menu_items(self, status_icon):
        if status_icon._impl.native.menu:
            return [
                {
                    "": "---",
                    "About Toga Testbed": "**ABOUT**",
                    "Quit Toga Testbed": "**EXIT**",
                }.get(str(item.title), str(item.title))
                for item in status_icon._impl.native.menu.itemArray
            ]
        else:
            # It's a button status item
            return None

    def activate_status_icon_button(self, item_id):
        self.app.status_icons[item_id]._impl.native.button.performClick(None)

    def activate_status_menu_item(self, item_id, title):
        item = self.app.status_icons[item_id]._impl.native.menu.itemWithTitle(title)
        send_message(
            self.app._impl.native.delegate,
            item.action,
            item,
            restype=None,
            argtypes=[objc_id],
        )
