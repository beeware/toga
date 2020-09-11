from toga.keys import Key
from .libs import WinForms


def winforms_key_to_toga(key, modifier):
    key = WINFORMS_KEYS_MAP.get(key, None)
    modifier = WINFORMS_MODIFIERS_MAP.get(modifier, None)
    if key is None:
        return None
    if modifier is None:
        return key
    return modifier + key


WINFORMS_MODIFIERS_MAP = {
    WinForms.Keys.Control: Key.MOD_1,
    WinForms.Keys.Alt: Key.MOD_2,
}
WINFORMS_KEYS_MAP = {
    WinForms.Keys.A: "a",
    WinForms.Keys.B: "b",
    WinForms.Keys.C: "c",
    WinForms.Keys.D: "d",
    WinForms.Keys.E: "e",
    WinForms.Keys.F: "f",
    WinForms.Keys.G: "g",
    WinForms.Keys.H: "h",
    WinForms.Keys.I: "i",
    WinForms.Keys.J: "j",
    WinForms.Keys.K: "k",
    WinForms.Keys.L: "l",
    WinForms.Keys.M: "m",
    WinForms.Keys.N: "n",
    WinForms.Keys.O: "o",
    WinForms.Keys.P: "p",
    WinForms.Keys.Q: "q",
    WinForms.Keys.R: "r",
    WinForms.Keys.S: "s",
    WinForms.Keys.T: "t",
    WinForms.Keys.U: "u",
    WinForms.Keys.V: "v",
    WinForms.Keys.W: "w",
    WinForms.Keys.X: "x",
    WinForms.Keys.Y: "y",
    WinForms.Keys.Z: "z",
}
