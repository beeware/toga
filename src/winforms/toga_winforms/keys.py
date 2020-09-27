from toga.keys import Key
from .libs import WinForms


def toga_to_winforms_key(key):
    code = 0
    for modifier, modifier_code in WINFORMS_MODIFIERS_MAP.items():
        if modifier.value in key:
            code |= modifier_code
            key = key.replace(modifier.value, "")
    key_code = WINFORMS_KEYS_MAP.get(key, None)
    if key_code is not None:
        code |= key_code
    return code


WINFORMS_MODIFIERS_MAP = {
    Key.MOD_1: WinForms.Keys.Control,
    Key.MOD_2: WinForms.Keys.Alt,
}
WINFORMS_KEYS_MAP = {
    Key.PLUS.value: WinForms.Keys.Oemplus,
    Key.MINUS.value: WinForms.Keys.OemMinus,
    "a": WinForms.Keys.A,
    "b": WinForms.Keys.B,
    "c": WinForms.Keys.C,
    "d": WinForms.Keys.D,
    "e": WinForms.Keys.E,
    "f": WinForms.Keys.F,
    "g": WinForms.Keys.G,
    "h": WinForms.Keys.H,
    "i": WinForms.Keys.I,
    "j": WinForms.Keys.J,
    "k": WinForms.Keys.K,
    "l": WinForms.Keys.L,
    "m": WinForms.Keys.M,
    "n": WinForms.Keys.N,
    "o": WinForms.Keys.O,
    "p": WinForms.Keys.P,
    "q": WinForms.Keys.Q,
    "r": WinForms.Keys.R,
    "s": WinForms.Keys.S,
    "t": WinForms.Keys.T,
    "u": WinForms.Keys.U,
    "v": WinForms.Keys.V,
    "w": WinForms.Keys.W,
    "x": WinForms.Keys.X,
    "y": WinForms.Keys.Y,
    "z": WinForms.Keys.Z,
}
