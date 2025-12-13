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
    async def redraw(self, message=None, delay=0):
        if toga.App.app.run_slow:
            delay = max(1, delay)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)
        else:
            QApplication.processEvents()

    def assert_image_size(self, image_size, size, screen):
        assert [s * screen._impl.native.devicePixelRatio() for s in size] == approx(
            image_size, abs=1
        )

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
