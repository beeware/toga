from toga.keys import Key

from toga_cocoa.libs import (
    NSEventModifierFlagCapsLock,
    NSEventModifierFlagShift,
    NSEventModifierFlagControl,
    NSEventModifierFlagOption,
    NSEventModifierFlagCommand,
)

######################################################################
# Utilities to convert Cocoa constants to Toga ones
######################################################################

def modified_key(key, shift=None):
    def mod_fn(modifierFlags):
        if modifierFlags & NSEventModifierFlagShift:
            return shift
        else:
            return key
    return mod_fn

def toga_key(keyCode, modifierFlags):
    key = {
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
        18: modified_key(Key._1, shift=Key.EXCLAMATION)(modifierFlags),
        19: modified_key(Key._2, shift=Key.AT)(modifierFlags),
        20: modified_key(Key._3, shift=Key.HASH)(modifierFlags),
        21: modified_key(Key._4, shift=Key.DOLLAR)(modifierFlags),
        22: modified_key(Key._6, shift=Key.CARET)(modifierFlags),
        23: modified_key(Key._5, shift=Key.PERCENT)(modifierFlags),
        24: Key.EQUAL,
        24: Key.PLUS,
        25: modified_key(Key._9, shift=Key.OPEN_PARENTHESIS)(modifierFlags),
        26: modified_key(Key._7, shift=Key.AND)(modifierFlags),
        27: modified_key(Key.MINUS, shift=Key.UNDERSCORE)(modifierFlags),
        28: modified_key(Key._8, shift=Key.ASTERISK)(modifierFlags),
        29: modified_key(Key._0, shift=Key.CLOSE_PARENTHESIS)(modifierFlags),
        30: Key.CLOSE_BRACKET,
        31: Key.O,
        32: Key.U,
        33: Key.OPEN_BRACKET,
        34: Key.I,
        35: Key.P,
        36: Key.ENTER,
        37: Key.L,
        38: Key.J,
        39: Key.DOUBLE_QUOTE,
        39: Key.QUOTE,
        40: Key.K,
        41: modified_key(Key.COLON, shift=Key.SEMICOLON)(modifierFlags),
        42: Key.BACKSLASH,
        43: modified_key(Key.COMMA, shift=Key.LESS_THAN)(modifierFlags),
        44: modified_key(Key.SLASH, shift=Key.QUESTION)(modifierFlags),
        45: Key.N,
        46: Key.M,
        47: modified_key(Key.FULL_STOP, shift=Key.GREATER_THAN)(modifierFlags),
        48: Key.TAB,
        49: Key.SPACE,
        50: modified_key(Key.BACK_QUOTE, shift=Key.TILDE)(modifierFlags),
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

    }.get(keyCode, None)

    modifiers = set()

    if modifierFlags & NSEventModifierFlagCapsLock:
        modifiers.add(Key.CAPS_LOCK)
    if modifierFlags & NSEventModifierFlagShift:
        modifiers.add(Key.SHIFT)
    if modifierFlags & NSEventModifierFlagControl:
        modifiers.add(Key.CONTROL)
    if modifierFlags & NSEventModifierFlagOption:
        modifiers.add(Key.OPTION)
    if modifierFlags & NSEventModifierFlagCommand:
        modifiers.add(Key.COMMAND)

    return {
        'key': key,
        'modifiers': modifiers
    }
