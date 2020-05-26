from toga import Key

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
        return key
    return mod_fn


def toga_key(event):
    """Convert a Cocoa NSKeyEvent into a Toga event."""
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
        18: modified_key(Key._1, shift=Key.EXCLAMATION)(event.modifierFlags),
        19: modified_key(Key._2, shift=Key.AT)(event.modifierFlags),
        20: modified_key(Key._3, shift=Key.HASH)(event.modifierFlags),
        21: modified_key(Key._4, shift=Key.DOLLAR)(event.modifierFlags),
        22: modified_key(Key._6, shift=Key.CARET)(event.modifierFlags),
        23: modified_key(Key._5, shift=Key.PERCENT)(event.modifierFlags),
        24: modified_key(Key.PLUS, shift=Key.EQUAL)(event.modifierFlags),
        25: modified_key(Key._9, shift=Key.OPEN_PARENTHESIS)(event.modifierFlags),
        26: modified_key(Key._7, shift=Key.AMPERSAND)(event.modifierFlags),
        27: modified_key(Key.MINUS, shift=Key.UNDERSCORE)(event.modifierFlags),
        28: modified_key(Key._8, shift=Key.ASTERISK)(event.modifierFlags),
        29: modified_key(Key._0, shift=Key.CLOSE_PARENTHESIS)(event.modifierFlags),
        30: Key.CLOSE_BRACKET,
        31: Key.O,
        32: Key.U,
        33: Key.OPEN_BRACKET,
        34: Key.I,
        35: Key.P,
        36: Key.ENTER,
        37: Key.L,
        38: Key.J,
        39: modified_key(Key.QUOTE, shift=Key.DOUBLE_QUOTE)(event.modifierFlags),
        40: Key.K,
        41: modified_key(Key.COLON, shift=Key.SEMICOLON)(event.modifierFlags),
        42: Key.BACKSLASH,
        43: modified_key(Key.COMMA, shift=Key.LESS_THAN)(event.modifierFlags),
        44: modified_key(Key.SLASH, shift=Key.QUESTION)(event.modifierFlags),
        45: Key.N,
        46: Key.M,
        47: modified_key(Key.FULL_STOP, shift=Key.GREATER_THAN)(event.modifierFlags),
        48: Key.TAB,
        49: Key.SPACE,
        50: modified_key(Key.BACK_QUOTE, shift=Key.TILDE)(event.modifierFlags),
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
    }.get(event.keyCode, None)

    modifiers = set()

    if event.modifierFlags & NSEventModifierFlagCapsLock:
        modifiers.add(Key.CAPSLOCK)
    if event.modifierFlags & NSEventModifierFlagShift:
        modifiers.add(Key.SHIFT)
    if event.modifierFlags & NSEventModifierFlagCommand:
        modifiers.add(Key.MOD_1)
    if event.modifierFlags & NSEventModifierFlagOption:
        modifiers.add(Key.MOD_2)
    if event.modifierFlags & NSEventModifierFlagControl:
        modifiers.add(Key.MOD_3)

    return {
        'key': key,
        'modifiers': modifiers
    }


COCOA_KEY_CODES = {
    Key.ESCAPE: "%c" % 0x001b,
    Key.TAB: "%c" % 0x0009,

    Key.BACKSPACE: "%c" % 0x0008,
    Key.ENTER: "%c" % 0x000d,

    Key.F1: "",  # TODO
    Key.F2: "",  # TODO
    Key.F3: "",  # TODO
    Key.F4: "",  # TODO
    Key.F5: "",  # TODO
    Key.F6: "",  # TODO
    Key.F7: "",  # TODO
    Key.F8: "",  # TODO
    Key.F9: "",  # TODO
    Key.F10: "",  # TODO
    Key.F11: "",  # TODO
    Key.F12: "",  # TODO
    Key.F13: "",  # TODO
    Key.F14: "",  # TODO
    Key.F15: "",  # TODO
    Key.F16: "",  # TODO
    Key.F17: "",  # TODO
    Key.F18: "",  # TODO
    Key.F19: "",  # TODO

    Key.EJECT: "",  # TODO

    Key.HOME: "%c" % 0x2196,
    Key.END: "%c" % 0x2198,
    Key.DELETE: "%c" % 0x007f,
    Key.PAGE_UP: "%c" % 0x21de,
    Key.PAGE_DOWN: "%c" % 0x21df,

    Key.UP: "%c" % 0x001e,
    Key.DOWN: "%c" % 0x001f,
    Key.LEFT: "%c" % 0x001c,
    Key.RIGHT: "%c" % 0x001d,

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
    Key.NUMPAD_DECIMAL_POINT: "",  # TODO
    Key.NUMPAD_DIVIDE: "",  # TODO
    Key.NUMPAD_ENTER: "",  # TODO
    Key.NUMPAD_EQUAL: "",  # TODO
    Key.NUMPAD_MINUS: "",  # TODO
    Key.NUMPAD_MULTIPLY: "",  # TODO
    Key.NUMPAD_PLUS: "",  # TODO
}

COCOA_MODIFIERS = {
    Key.SHIFT: NSEventModifierFlagShift,
    Key.CAPSLOCK: NSEventModifierFlagCapsLock,

    Key.MOD_1: NSEventModifierFlagCommand,
    Key.MOD_2: NSEventModifierFlagOption,
    Key.MOD_3: NSEventModifierFlagControl,
}


def cocoa_key(shortcut):
    """Convert a Toga shortcut definition into Cocoa key equivalents"""
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
            key = key.replace(mod.value, '')
            modifiers |= mask

    return (key, modifiers)
