"""Utilities to convert Cocoa constants to Toga ones."""

from toga import Key
from toga_cocoa.libs import (
    NSEventModifierFlagCommand,
    NSEventModifierFlagControl,
    NSEventModifierFlagOption,
    NSEventModifierFlagShift,
)

# A map of Cocoa keycodes to Toga key values, when no Shift is pressed
TOGA_KEYS = {
    0: Key.A,
    1: Key.S,
    2: Key.D,
    3: Key.F,
    4: Key.H,
    5: Key.G,
    6: Key.Z,
    7: Key.X,
    8: Key.C,
    9: Key.V,
    11: Key.B,
    12: Key.Q,
    13: Key.W,
    14: Key.E,
    15: Key.R,
    16: Key.Y,
    17: Key.T,
    18: Key._1,
    19: Key._2,
    20: Key._3,
    21: Key._4,
    22: Key._6,
    23: Key._5,
    24: Key.PLUS,
    25: Key._9,
    26: Key._7,
    27: Key.MINUS,
    28: Key._8,
    29: Key._0,
    30: Key.CLOSE_BRACKET,
    31: Key.O,
    32: Key.U,
    33: Key.OPEN_BRACKET,
    34: Key.I,
    35: Key.P,
    36: Key.ENTER,
    37: Key.L,
    38: Key.J,
    39: Key.QUOTE,
    40: Key.K,
    41: Key.SEMICOLON,
    42: Key.BACKSLASH,
    43: Key.COMMA,
    44: Key.SLASH,
    45: Key.N,
    46: Key.M,
    47: Key.FULL_STOP,
    48: Key.TAB,
    49: Key.SPACE,
    50: Key.BACK_QUOTE,
    51: Key.BACKSPACE,
    53: Key.ESCAPE,
    65: Key.NUMPAD_DECIMAL_POINT,
    67: Key.NUMPAD_MULTIPLY,
    69: Key.NUMPAD_PLUS,
    71: Key.NUMPAD_CLEAR,
    75: Key.NUMPAD_DIVIDE,
    76: Key.NUMPAD_ENTER,
    78: Key.NUMPAD_MINUS,
    81: Key.NUMPAD_EQUAL,
    82: Key.NUMPAD_0,
    83: Key.NUMPAD_1,
    84: Key.NUMPAD_2,
    85: Key.NUMPAD_3,
    86: Key.NUMPAD_4,
    87: Key.NUMPAD_5,
    88: Key.NUMPAD_6,
    89: Key.NUMPAD_7,
    91: Key.NUMPAD_8,
    92: Key.NUMPAD_9,
    # : Key.F4,
    96: Key.F5,
    97: Key.F7,
    98: Key.F5,
    99: Key.F3,
    100: Key.F8,
    101: Key.F9,
    109: Key.F9,
    115: Key.HOME,
    116: Key.PAGE_UP,
    117: Key.DELETE,
    119: Key.END,
    120: Key.F2,
    121: Key.PAGE_DOWN,
    122: Key.F1,
    123: Key.LEFT,
    124: Key.RIGHT,
    125: Key.DOWN,
    126: Key.UP,
}

# Keys that have a different Toga key when Shift is pressed.
TOGA_SHIFT_MODIFIED = {
    Key.BACK_QUOTE: Key.TILDE,
    Key._1: Key.EXCLAMATION,
    Key._2: Key.AT,
    Key._3: Key.HASH,
    Key._4: Key.DOLLAR,
    Key._5: Key.PERCENT,
    Key._6: Key.CARET,
    Key._7: Key.AMPERSAND,
    Key._8: Key.ASTERISK,
    Key._9: Key.OPEN_PARENTHESIS,
    Key._0: Key.CLOSE_PARENTHESIS,
    Key.MINUS: Key.UNDERSCORE,
    Key.EQUAL: Key.PLUS,
    Key.CLOSE_BRACKET: Key.CLOSE_BRACE,
    Key.OPEN_BRACKET: Key.OPEN_BRACE,
    Key.BACKSLASH: Key.PIPE,
    Key.QUOTE: Key.DOUBLE_QUOTE,
    Key.SEMICOLON: Key.COLON,
    Key.COMMA: Key.LESS_THAN,
    Key.FULL_STOP: Key.GREATER_THAN,
    Key.SLASH: Key.QUESTION,
}


def toga_key(event):
    """Convert a Cocoa NSKeyEvent into a Toga event."""
    natural_key = TOGA_KEYS.get(event.keyCode, None)
    if event.modifierFlags & NSEventModifierFlagShift:
        try:
            key = TOGA_SHIFT_MODIFIED[natural_key]
        except KeyError:
            key = natural_key
    else:
        key = natural_key

    modifiers = set()

    # Only apply a shift modifier for the a/A case.
    # keys like ! that inherently need shift don't return as modified.
    if event.modifierFlags & NSEventModifierFlagShift and key == natural_key:
        modifiers.add(Key.SHIFT)
    if event.modifierFlags & NSEventModifierFlagCommand:
        modifiers.add(Key.MOD_1)
    if event.modifierFlags & NSEventModifierFlagOption:
        modifiers.add(Key.MOD_2)
    if event.modifierFlags & NSEventModifierFlagControl:
        modifiers.add(Key.MOD_3)

    return {"key": key, "modifiers": modifiers}


COCOA_KEY_CODES = {
    Key.ESCAPE: chr(0x001B),
    Key.TAB: chr(0x0009),
    Key.BACKSPACE: chr(0x0008),
    Key.ENTER: chr(0x000D),
    Key.F1: chr(0xF704),
    Key.F2: chr(0xF705),
    Key.F3: chr(0xF706),
    Key.F4: chr(0xF707),
    Key.F5: chr(0xF708),
    Key.F6: chr(0xF709),
    Key.F7: chr(0xF70A),
    Key.F8: chr(0xF70B),
    Key.F9: chr(0xF70C),
    Key.F10: chr(0xF70D),
    Key.F11: chr(0xF70E),
    Key.F12: chr(0xF70F),
    Key.F13: chr(0xF710),
    Key.F14: chr(0xF711),
    Key.F15: chr(0xF712),
    Key.F16: chr(0xF713),
    Key.F17: chr(0xF714),
    Key.F18: chr(0xF715),
    Key.F19: chr(0xF716),
    Key.EJECT: "",  # TODO
    Key.HOME: chr(0xF729),
    Key.END: chr(0xF72B),
    Key.DELETE: chr(0xF728),
    Key.PAGE_UP: chr(0xF72C),
    Key.PAGE_DOWN: chr(0xF72D),
    Key.UP: chr(0xF700),
    Key.DOWN: chr(0xF701),
    Key.LEFT: chr(0xF702),
    Key.RIGHT: chr(0xF703),
    Key.NUMPAD_0: "0",
    Key.NUMPAD_1: "1",
    Key.NUMPAD_2: "2",
    Key.NUMPAD_3: "3",
    Key.NUMPAD_4: "4",
    Key.NUMPAD_5: "5",
    Key.NUMPAD_6: "6",
    Key.NUMPAD_7: "7",
    Key.NUMPAD_8: "8",
    Key.NUMPAD_9: "9",
    Key.NUMPAD_CLEAR: "",  # TODO
    Key.NUMPAD_DECIMAL_POINT: ".",
    Key.NUMPAD_DIVIDE: "/",
    Key.NUMPAD_ENTER: chr(0x000D),
    Key.NUMPAD_EQUAL: "=",
    Key.NUMPAD_MINUS: "-",
    Key.NUMPAD_MULTIPLY: "*",
    Key.NUMPAD_PLUS: "+",
}

COCOA_MODIFIERS = {
    Key.SHIFT: NSEventModifierFlagShift,
    Key.MOD_1: NSEventModifierFlagCommand,
    Key.MOD_2: NSEventModifierFlagOption,
    Key.MOD_3: NSEventModifierFlagControl,
}


def cocoa_key(shortcut):
    """Convert a Toga shortcut definition into Cocoa key equivalents."""
    modifiers = 0
    # Convert the shortcut into string form.
    try:
        key = shortcut.value
    except AttributeError:
        key = shortcut

    # Replace any <> special keys with the character equivalents
    # understood by Cocoa
    for code, equiv in COCOA_KEY_CODES.items():
        key = key.replace(code.value, equiv)

    # Remove any modifier definitions mentions, and
    # add them to the modifier mask.
    for mod, mask in COCOA_MODIFIERS.items():
        if mod.value in key:
            key = key.replace(mod.value, "")
            modifiers |= mask

    # If the remaining key string is upper case, add a shift modifier.
    if key.isupper():
        modifiers |= NSEventModifierFlagShift

    return key, modifiers
