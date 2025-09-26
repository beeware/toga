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
}

MODIFIER_MAP = {
    "shift": Qt.ShiftModifier,
    "ctrl": Qt.ControlModifier,
    "alt": Qt.AltModifier,
}


class BaseProbe(DialogsMixin):
    async def redraw(self, message=None, delay=0):
        for widget in QApplication.allWidgets():
            widget.repaint()  # this is immediate and will block

        if toga.App.app.run_slow:
            delay = max(1, delay)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert (
            approx(image_size, abs=1) == size * screen._impl.native.devicePixelRatio()
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
