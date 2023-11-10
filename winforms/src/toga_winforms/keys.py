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
    "+": WinForms.Keys.Oemplus,
    "-": WinForms.Keys.OemMinus,
}
WINFORMS_KEYS.update(
    {str(digit): getattr(WinForms.Keys, f"D{digit}") for digit in range(10)}
)

SHIFTED_KEYS = {symbol: number for symbol, number in zip("!@#$%^&*()", "1234567890")}
SHIFTED_KEYS.update(
    {lower.upper(): lower for lower in ascii_lowercase},
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
