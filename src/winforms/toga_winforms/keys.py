import operator
from functools import reduce
from string import ascii_uppercase

from toga.keys import Key
from .libs import WinForms


def toga_to_winforms_key(key):
    codes = []
    for modifier, modifier_code in WINFORMS_NON_PRINTABLES_MAP.items():
        if modifier.value in key:
            codes.append(modifier_code)
            key = key.replace(modifier.value, "")
    key_code = WINFORMS_KEYS_MAP.get(key, None)
    if key_code is not None:
        codes.append(key_code)
    return reduce(operator.or_, codes)


WINFORMS_NON_PRINTABLES_MAP = {
    Key.MOD_1: WinForms.Keys.Control,
    Key.MOD_2: WinForms.Keys.Alt,
}
WINFORMS_NON_PRINTABLES_MAP.update({
    getattr(Key, modifier.upper()): getattr(WinForms.Keys, modifier.title())
    for modifier in ["shift", "up", "down", "left", "right", "home"]
})

WINFORMS_KEYS_MAP = {
    Key.PLUS.value: WinForms.Keys.Oemplus,
    Key.MINUS.value: WinForms.Keys.OemMinus,
}
WINFORMS_KEYS_MAP.update({
    getattr(Key, letter).value: getattr(WinForms.Keys, letter)
    for letter in ascii_uppercase
})
