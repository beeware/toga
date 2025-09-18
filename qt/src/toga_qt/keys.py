import re
from string import ascii_lowercase

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence

from toga.keys import Key

QT_MODIFIERS = {
    Key.MOD_1: Qt.ControlModifier,
    Key.MOD_2: Qt.AltModifier,
    Key.MOD_3: Qt.MetaModifier,
    Key.SHIFT: Qt.ShiftModifier,
}

# [sweating intensifies]
# TODO: Refs https://forum.qt.io/topic/162828/how-do-i-check-for-shift-tab
QT_KEYS = {
    Key.ESCAPE.value: Qt.Key_Escape,
    Key.BACK_QUOTE.value: Qt.Key_QuoteLeft,  # Why quoteleft, are the Qt devs up to TeX?
    Key.MINUS.value: Qt.Key_Minus,
    Key.EQUAL.value: Qt.Key_Equal,
    Key.CAPSLOCK.value: Qt.Key_CapsLock,
    Key.TAB.value: Qt.Key_Tab,
    Key.OPEN_BRACKET.value: Qt.Key_BracketLeft,
    Key.CLOSE_BRACKET.value: Qt.Key_BracketRight,
    Key.BACKSLASH.value: Qt.Key_Backslash,
    Key.SEMICOLON.value: Qt.Key_Semicolon,
    Key.QUOTE.value: Qt.Key_QuoteDbl,  # why shifted form?
    Key.COMMA.value: Qt.Key_Comma,
    Key.FULL_STOP.value: Qt.Key_Period,
    Key.SLASH.value: Qt.Key_Slash,
    Key.SPACE.value: Qt.Key_Space,
    Key.PAGE_UP.value: Qt.Key_PageUp,
    Key.PAGE_DOWN.value: Qt.Key_PageDown,
    Key.INSERT.value: Qt.Key_Insert,
    Key.DELETE.value: Qt.Key_Delete,
    Key.HOME.value: Qt.Key_Home,
    Key.END.value: Qt.Key_End,
    Key.UP.value: Qt.Key_Up,
    Key.DOWN.value: Qt.Key_Down,
    Key.LEFT.value: Qt.Key_Left,
    Key.RIGHT.value: Qt.Key_Right,
    Key.NUMLOCK.value: Qt.Key_NumLock,
    Key.SCROLLLOCK.value: Qt.Key_ScrollLock,
    Key.MENU.value: Qt.Key_Menu,
}


QT_KEYS.update({str(digit): getattr(Qt, f"Key_{digit}") for digit in range(10)})

QT_KEYS.update(
    {getattr(Key, f"F{num}").value: getattr(Qt, f"Key_F{num}") for num in range(1, 20)}
)

QT_KEYS.update(
    {
        getattr(Key, letter).value: getattr(Qt, f"Key_{letter}")
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    }
)

NUMPAD_KEYS = {
    Key.NUMPAD_DECIMAL_POINT.value: Qt.Key_Period,
}

NUMPAD_KEYS.update(
    {
        getattr(Key, f"NUMPAD_{digit}").value: getattr(Key, f"_{digit}").value
        for digit in range(10)
    }
)

NUMPAD_KEYS_REV = {v: k for k, v in NUMPAD_KEYS.items()}

SHIFTED_KEYS = dict(zip("!@#$%^&*()", "1234567890"))
SHIFTED_KEYS.update(
    {
        "~": "`",
        "_": "-",
        "+": "=",
        "{": "[",
        "}": "]",
        "|": "\\",
        ":": ";",
        '"': "'",
        "<": ",",
        ">": ".",
        "?": "/",
    }
)
TEST_SHIFTED_KEYS = {v: k for k, v in SHIFTED_KEYS.items()}

SHIFTED_KEYS.update({lower.upper(): lower for lower in ascii_lowercase})


def toga_to_qt_key(key):
    # Convert a Key object into QKeySequence form.
    try:
        key = key.value
    except AttributeError:
        pass

    codes = Qt.NoModifier
    for modifier, modifier_code in QT_MODIFIERS.items():
        if modifier.value in key:
            codes |= modifier_code
            key = key.replace(modifier.value, "")

    if regular := NUMPAD_KEYS.get(key):
        key = regular
        codes |= Qt.KeypadModifier

    if lower := SHIFTED_KEYS.get(key):
        key = lower
        codes |= Qt.ShiftModifier

    try:
        codes |= QT_KEYS[key]
    except KeyError:
        if match := re.fullmatch(r"<(.+)>", key):
            key = match[1]
        try:
            codes |= getattr(Qt, key.title())
        except AttributeError:  # pragma: no cover
            raise ValueError(f"unknown key: {key!r}") from None

    return QKeySequence(codes)


def qt_to_toga_key(code):
    modifiers = set()
    native_mods = code[0].keyboardModifiers()
    for mod_key, qt_mod in QT_MODIFIERS.items():
        if native_mods & qt_mod:
            modifiers.add(mod_key)

    qt_key_code = code[0].key()
    qt_to_toga = {v: k for k, v in QT_KEYS.items()}
    toga_value = qt_to_toga.get(qt_key_code)

    # Qt decomposes shifted characters
    if Key.SHIFT in modifiers and toga_value in TEST_SHIFTED_KEYS:
        modifiers.remove(Key.SHIFT)
        toga_value = TEST_SHIFTED_KEYS[toga_value]
    # Qt uses a separate modifier for numpad
    if native_mods & Qt.KeypadModifier:
        toga_value = NUMPAD_KEYS_REV[toga_value]

    return {"key": Key(toga_value), "modifiers": modifiers}
