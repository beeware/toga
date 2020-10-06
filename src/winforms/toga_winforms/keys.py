from toga.keys import Key
from .libs import WinForms
from string import ascii_uppercase


def toga_to_winforms_key(key):
    code = 0
    for modifier, modifier_code in WINFORMS_NON_PRINTABLES_MAP.items():
        if modifier.value in key:
            code |= modifier_code
            key = key.replace(modifier.value, "")
    key_code = WINFORMS_KEYS_MAP.get(key, None)
    if key_code is not None:
        code |= key_code
    return code


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
