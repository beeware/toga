import operator
import re
from functools import reduce

import System.Windows.Forms as WinForms

from toga.keys import Key

WINFORMS_MODIFIERS = {
    Key.MOD_1: WinForms.Keys.Control,
    Key.MOD_2: WinForms.Keys.Alt,
    Key.SHIFT: WinForms.Keys.Shift,
}

WINFORMS_KEYS_MAP = {
    Key.PLUS.value: WinForms.Keys.Oemplus,
    Key.MINUS.value: WinForms.Keys.OemMinus,
}
WINFORMS_KEYS_MAP.update(
    {str(digit): getattr(WinForms.Keys, f"D{digit}") for digit in range(10)}
)


def toga_to_winforms_key(key):
    codes = []
    for modifier, modifier_code in WINFORMS_MODIFIERS.items():
        if modifier.value in key:
            codes.append(modifier_code)
            key = key.replace(modifier.value, "")

    try:
        codes.append(WINFORMS_KEYS_MAP[key])
    except KeyError:
        if match := re.fullmatch(r"<(.+)>", key):
            key = match[1]
        try:
            codes.append(getattr(WinForms.Keys, key.title()))
        except AttributeError:  # pragma: no cover
            raise ValueError(f"unknown key: {key!r}") from None

    return reduce(operator.or_, codes)
