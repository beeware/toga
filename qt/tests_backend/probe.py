import asyncio

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication
from pytest import approx

import toga

from .dialogs import DialogsMixin

SPECIAL_KEY_MAP = {
    " ": Qt.Key_Space,
    "-": Qt.Key_Minus,
    ".": Qt.Key_Period,
    "\n": Qt.Key_Return,
    "<esc>": Qt.Key_Escape,
    "'": Qt.Key_Apostrophe,
    '"': Qt.Key_QuoteDbl,
    "<backspace>": Qt.Key_Backspace,
}

MODIFIER_MAP = {
    "shift": Qt.ShiftModifier,
    "ctrl": Qt.ControlModifier,
    "alt": Qt.AltModifier,
}


class BaseProbe(DialogsMixin):
    async def redraw(self, message=None, delay=0, wait_for=None):
        # If we're running slow, or we have a wait condition,
        # wait for at least a second
        if toga.App.app.run_slow or wait_for:
            delay = max(1, delay)

        if delay or wait_for:
            print("Waiting for redraw" if message is None else message)
            if toga.App.app.run_slow or wait_for is None:
                await asyncio.sleep(delay)
            else:
                delta = 0.1
                interval = 0.0
                while not wait_for() and interval < delay:
                    await asyncio.sleep(delta)
                    interval += delta
        else:
            QApplication.processEvents()

    def assert_image_size(self, image_size, size, screen, window=None):
        if window is None:
            # This is unreliable on Wayland; however, the only image
            # size assertion without a window is testing the image of
            # the whole screen, which is not supported on Wayland yet.
            pixel_ratio = screen._impl.native.devicePixelRatio()
        else:
            pixel_ratio = window._impl.native.windowHandle().devicePixelRatio()

        assert [s * pixel_ratio for s in size] == approx(image_size, abs=1)

    async def type_character(self, char, *, shift=False, ctrl=False, alt=False):
        widget = QApplication.focusWidget()
        if widget is None:
            raise RuntimeError("No widget has focus to receive key events.")

        key = SPECIAL_KEY_MAP.get(char)
        if key is None:
            if len(char) == 1:
                key = Qt.Key(ord(char.upper()))
            else:
                raise ValueError(f"Unsupported character: {char!r}")
        modifiers = Qt.NoModifier
        if shift:
            modifiers |= Qt.ShiftModifier
        if ctrl:
            modifiers |= Qt.ControlModifier
        if alt:
            modifiers |= Qt.AltModifier
        press = QKeyEvent(QEvent.KeyPress, key, modifiers, char)
        release = QKeyEvent(QEvent.KeyRelease, key, modifiers, char)
        QApplication.sendEvent(widget, press)
        QApplication.sendEvent(widget, release)

    def _menu_item(self, path):
        # Do not let the test fail if there is no focussed window,
        # though we'd prefer that because users do it.
        menu_bar = (
            toga.App.app.current_window or toga.App.app.main_window
        )._impl.native.menuBar()
        current_menu = menu_bar
        for label in path:
            for action in current_menu.actions():
                if action.text() == label:
                    if action.menu():
                        current_menu = action.menu()
                    else:
                        return action
                    break
            else:
                raise AssertionError(f"Menu path {path} not found")
        return current_menu

    def _activate_menu_item(self, path):
        item = self._menu_item(path)
        item.trigger()
