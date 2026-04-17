from string import ascii_lowercase

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence

from toga.keys import Key

QT_MODIFIERS = {
    Key.MOD_1: Qt.KeyboardModifier.ControlModifier,
    Key.MOD_2: Qt.KeyboardModifier.AltModifier,
    Key.MOD_3: Qt.KeyboardModifier.MetaModifier,
    Key.SHIFT: Qt.KeyboardModifier.ShiftModifier,
}

# Note: In Qt's key combos there's certain ones like Key_Copy or Key_BackTab.
# Empirical evidence shows that they exists to abstracts the shortcuts in a
# cross-platform way; they are not needed since the Qt backend is for Linux
# only.
QT_KEYS = {
    Key.EXCLAMATION.value: Qt.Key.Key_Exclam,
    Key.AT.value: Qt.Key.Key_At,
    Key.HASH.value: Qt.Key.Key_NumberSign,
    Key.DOLLAR.value: Qt.Key.Key_Dollar,
    Key.PERCENT.value: Qt.Key.Key_Percent,
    Key.CARET.value: Qt.Key.Key_AsciiCircum,
    Key.AMPERSAND.value: Qt.Key.Key_Ampersand,
    Key.ASTERISK.value: Qt.Key.Key_Asterisk,
    Key.OPEN_PARENTHESIS.value: Qt.Key.Key_ParenLeft,
    Key.CLOSE_PARENTHESIS.value: Qt.Key.Key_ParenRight,
    Key.MINUS.value: Qt.Key.Key_Minus,
    Key.UNDERSCORE.value: Qt.Key.Key_Underscore,
    Key.EQUAL.value: Qt.Key.Key_Equal,
    Key.PLUS.value: Qt.Key.Key_Plus,
    Key.OPEN_BRACKET.value: Qt.Key.Key_BracketLeft,
    Key.CLOSE_BRACKET.value: Qt.Key.Key_BracketRight,
    Key.OPEN_BRACE.value: Qt.Key.Key_BraceLeft,
    Key.CLOSE_BRACE.value: Qt.Key.Key_BraceRight,
    Key.BACKSLASH.value: Qt.Key.Key_Backslash,
    Key.PIPE.value: Qt.Key.Key_Bar,
    Key.SEMICOLON.value: Qt.Key.Key_Semicolon,
    Key.COLON.value: Qt.Key.Key_Colon,
    Key.QUOTE.value: Qt.Key.Key_Apostrophe,
    Key.DOUBLE_QUOTE.value: Qt.Key.Key_QuoteDbl,
    Key.COMMA.value: Qt.Key.Key_Comma,
    Key.LESS_THAN.value: Qt.Key.Key_Less,
    Key.FULL_STOP.value: Qt.Key.Key_Period,
    Key.GREATER_THAN.value: Qt.Key.Key_Greater,
    Key.SLASH.value: Qt.Key.Key_Slash,
    Key.QUESTION.value: Qt.Key.Key_Question,
    Key.BACK_QUOTE.value: Qt.Key.Key_QuoteLeft,
    Key.TILDE.value: Qt.Key.Key_AsciiTilde,
    Key.ESCAPE.value: Qt.Key.Key_Escape,
    Key.TAB.value: Qt.Key.Key_Tab,
    Key.SPACE.value: Qt.Key.Key_Space,
    Key.BACKSPACE.value: Qt.Key.Key_Backspace,
    Key.ENTER.value: Qt.Key.Key_Return,
    Key.CAPSLOCK.value: Qt.Key.Key_CapsLock,
    Key.SHIFT.value: Qt.Key.Key_Shift,
    Key.MOD_1: Qt.Key.Key_Control,
    Key.MOD_2: Qt.Key.Key_Alt,
    Key.MOD_3: Qt.Key.Key_Meta,
    Key.HOME.value: Qt.Key.Key_Home,
    Key.END.value: Qt.Key.Key_End,
    Key.INSERT.value: Qt.Key.Key_Insert,
    Key.DELETE.value: Qt.Key.Key_Delete,
    Key.PAGE_UP.value: Qt.Key.Key_PageUp,
    Key.PAGE_DOWN.value: Qt.Key.Key_PageDown,
    Key.UP.value: Qt.Key.Key_Up,
    Key.DOWN.value: Qt.Key.Key_Down,
    Key.LEFT.value: Qt.Key.Key_Left,
    Key.RIGHT.value: Qt.Key.Key_Right,
    Key.SCROLLLOCK.value: Qt.Key.Key_ScrollLock,
    Key.MENU.value: Qt.Key.Key_Menu,
    Key.BEGIN.value: Qt.Key.Key_MediaPlay,
    Key.PAUSE.value: Qt.Key.Key_MediaPause,
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
    Key.NUMLOCK.value: Qt.Key.Key_NumLock,
    Key.NUMPAD_DECIMAL_POINT.value: Qt.Key.Key_Period,
    Key.NUMPAD_ENTER.value: Qt.Key.Key_Enter,
}

NUMPAD_KEYS.update(
    {
        getattr(Key, f"NUMPAD_{digit}").value: getattr(Key, f"_{digit}").value
        for digit in range(10)
    }
)

NUMPAD_KEYS_REV = {v: k for k, v in NUMPAD_KEYS.items()}

SHIFTED_KEYS = dict(zip("!@#$%^&*()", "1234567890", strict=False))
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

QT_TO_TOGA = {v: k for k, v in QT_KEYS.items()}


def toga_to_qt_key(key):
    # Convert a Key object into QKeySequence form.
    try:
        key = key.value
    except AttributeError:
        pass

    codes = Qt.KeyboardModifier.NoModifier
    for modifier, modifier_code in QT_MODIFIERS.items():
        if modifier.value in key:
            codes |= modifier_code
            key = key.replace(modifier.value, "")

    if regular := NUMPAD_KEYS.get(key):
        key = regular
        codes |= Qt.KeyboardModifier.KeypadModifier

    if lower := SHIFTED_KEYS.get(key):
        key = lower
        codes |= Qt.KeyboardModifier.ShiftModifier

    try:
        codes |= QT_KEYS[key]
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
    toga_value = QT_TO_TOGA.get(qt_key_code)
    if toga_value is None:  # pragma: no cover
        # An unmapped key (frequently a bare modifier key)
        # These are not currently tested.
        return None

    # Qt uses a separate modifier for numpad
    if native_mods & Qt.KeyboardModifier.KeypadModifier:
        toga_value = NUMPAD_KEYS_REV[toga_value]

    # Qt decomposes shifted characters
    if Key.SHIFT in modifiers and toga_value in TEST_SHIFTED_KEYS:
        # I don't think this ever gets called on a US keyboard, as
        # toga_value holds the shifted value already
        modifiers.remove(Key.SHIFT)
        toga_value = TEST_SHIFTED_KEYS[toga_value]

    return {"key": Key(toga_value), "modifiers": modifiers}
