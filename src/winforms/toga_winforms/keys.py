import operator
from functools import reduce
from string import ascii_uppercase

from toga.keys import Key
from .libs import WinForms


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


TOGA_KEYS_MAP = {
    w: t
    for t, w in WINFORMS_KEYS_MAP.items()
}
TOGA_KEYS_MAP.update({
    getattr(WinForms.Keys, modifier.title()): getattr(Key, modifier.upper())
    for modifier in ["shift", "up", "down", "left", "right", "home"]
})


def toga_key(event):
    """Convert a Cocoa NSKeyEvent into a Toga event."""
    try:
        key = TOGA_KEYS_MAP[event.KeyCode]
    except KeyError:
        key = WINFORMS_NON_PRINTABLES_MAP
    modifiers = set()

    # if event.Capslock?:
    #     modifiers.add(Key.CAPSLOCK)
    if event.Shift:
        modifiers.add(Key.SHIFT)
    if event.Control:
        modifiers.add(Key.MOD_1)
    if event.Alt:
        modifiers.add(Key.MOD_2)
    # if event.Windows?:
        # modifiers.add(Key.MOD_3)

    return {
        'key': key,
        'modifiers': modifiers
    }
