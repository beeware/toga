import operator
import re
from functools import reduce
from string import ascii_lowercase

import System.Windows.Forms as WinForms

from toga.keys import Key

WINFORMS_MODIFIERS = {
    Key.MOD_1: WinForms.Keys.Control,
    Key.MOD_2: WinForms.Keys.Alt,
    Key.SHIFT: WinForms.Keys.Shift,
}

WINFORMS_KEYS = {
    Key.ESCAPE.value: WinForms.Keys.Escape,
    # Key.BACK_QUOTE.value: WinForms.Keys.Oemtilde,  # No idea what the code should be
    Key.MINUS.value: WinForms.Keys.OemMinus,
    Key.EQUAL.value: WinForms.Keys.Oemplus,
    Key.CAPSLOCK.value: WinForms.Keys.CapsLock,
    Key.TAB.value: WinForms.Keys.Tab,
    Key.OPEN_BRACKET.value: WinForms.Keys.OemOpenBrackets,
    Key.CLOSE_BRACKET.value: WinForms.Keys.OemCloseBrackets,
    Key.BACKSLASH.value: WinForms.Keys.OemQuotes,  # NFI what is going on here
    Key.SEMICOLON.value: WinForms.Keys.OemSemicolon,
    Key.QUOTE.value: WinForms.Keys.Oemtilde,  # NFI what is going on here
    Key.COMMA.value: WinForms.Keys.Oemcomma,
    Key.FULL_STOP.value: WinForms.Keys.OemPeriod,
    Key.SLASH.value: WinForms.Keys.OemQuestion,  # Key uses the shifted form
    Key.SPACE.value: WinForms.Keys.Space,
    Key.PAGE_UP.value: WinForms.Keys.PageUp,
    Key.PAGE_DOWN.value: WinForms.Keys.PageDown,
    Key.INSERT.value: WinForms.Keys.Insert,
    Key.DELETE.value: WinForms.Keys.Delete,
    Key.HOME.value: WinForms.Keys.Home,
    Key.END.value: WinForms.Keys.End,
    Key.UP.value: WinForms.Keys.Up,
    Key.DOWN.value: WinForms.Keys.Down,
    Key.LEFT.value: WinForms.Keys.Left,
    Key.RIGHT.value: WinForms.Keys.Right,
    Key.NUMLOCK.value: WinForms.Keys.NumLock,
    Key.NUMPAD_DECIMAL_POINT.value: WinForms.Keys.Decimal,
    Key.SCROLLLOCK.value: WinForms.Keys.Scroll,
    Key.MENU.value: WinForms.Keys.Menu,
}
WINFORMS_KEYS.update(
    {str(digit): getattr(WinForms.Keys, f"D{digit}") for digit in range(10)}
)
WINFORMS_KEYS.update(
    {
        getattr(Key, f"NUMPAD_{digit}").value: getattr(WinForms.Keys, f"NumPad{digit}")
        for digit in range(10)
    }
)

SHIFTED_KEYS = {symbol: number for symbol, number in zip("!@#$%^&*()", "1234567890")}
SHIFTED_KEYS.update(
    {lower.upper(): lower for lower in ascii_lowercase},
)
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


def toga_to_winforms_key(key):
    # Convert a Key object into string form.
    try:
        key = key.value
    except AttributeError:
        pass

    codes = []
    for modifier, modifier_code in WINFORMS_MODIFIERS.items():
        if modifier.value in key:
            codes.append(modifier_code)
            key = key.replace(modifier.value, "")

    if lower := SHIFTED_KEYS.get(key):
        key = lower
        codes.append(WinForms.Keys.Shift)

    try:
        codes.append(WINFORMS_KEYS[key])
    except KeyError:
        if match := re.fullmatch(r"<(.+)>", key):
            key = match[1]
        try:
            codes.append(getattr(WinForms.Keys, key.title()))
        except AttributeError:  # pragma: no cover
            raise ValueError(f"unknown key: {key!r}") from None

    return reduce(operator.or_, codes)


def toga_to_winforms_shortcut(key):
    # The Winforms key enum is... daft. The "oem" key values render as "Oem" or
    # "Oemcomma", so we need to *manually* set the display text for the key
    # shortcut.

    # Convert a Key object into string form.
    try:
        key = key.value
    except AttributeError:
        key = key

    # Replace modifiers with the Winforms text
    display = []
    for toga_keyval, winforms_keyval in [
        (Key.MOD_1.value, "Ctrl"),
        (Key.MOD_2.value, "Alt"),
        (Key.SHIFT.value, "Shift"),
    ]:
        if toga_keyval in key:
            display.append(winforms_keyval)
            key = key.replace(toga_keyval, "")

    if key == " ":
        display.append("Space")
    else:
        # Convert non-printable characters to printable
        if match := re.fullmatch(r"<(.+)>", key):
            key = match[1]

        # All remaining text is displayed in title case. Shift will already be
        # in the shortcut if it's an upper case letter; it's title() rather
        # than upper() because we want both a->A and esc -> Esc
        display.append(key.title())

    return "+".join(display)


def winforms_to_toga_key(code):
    modifiers = set()

    code_names = str(code).split(", ")
    for toga_mod, code in WINFORMS_MODIFIERS.items():
        try:
            code_names.remove(str(code))
        except ValueError:
            pass
        else:
            modifiers.add(toga_mod)

    assert len(code_names) == 1
    for toga_value, code in WINFORMS_KEYS.items():
        if str(code) == code_names[0]:
            break
    else:
        toga_value = code_names[0].lower()
        if len(toga_value) > 1:
            toga_value = f"<{toga_value}>"

    if (Key.SHIFT in modifiers) and (toga_value not in ascii_lowercase):
        for symbol, number in SHIFTED_KEYS.items():
            if toga_value == number:
                toga_value = symbol
                modifiers.remove(Key.SHIFT)

    return {"key": Key(toga_value), "modifiers": modifiers}
