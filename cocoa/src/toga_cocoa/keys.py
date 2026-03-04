"""Utilities to convert Cocoa constants to Toga ones."""

from toga import Key
from toga_cocoa.libs import (
    NSEventModifierFlagCommand,
    NSEventModifierFlagControl,
    NSEventModifierFlagOption,
    NSEventModifierFlagShift,
)

# Mapping from Cocoa Event.characters to toga.Key
NON_PRINTABLE_KEYS_TO_TOGA = {
    chr(0x001B): Key.ESCAPE,
    chr(0x0009): Key.TAB,
    chr(0x0008): Key.BACKSPACE,
    chr(0x000D): Key.ENTER,
    chr(0xF704): Key.F1,
    chr(0xF705): Key.F2,
    chr(0xF706): Key.F3,
    chr(0xF707): Key.F4,
    chr(0xF708): Key.F5,
    chr(0xF709): Key.F6,
    chr(0xF70A): Key.F7,
    chr(0xF70B): Key.F8,
    chr(0xF70C): Key.F9,
    chr(0xF70D): Key.F10,
    chr(0xF70E): Key.F11,
    chr(0xF70F): Key.F12,
    chr(0xF710): Key.F13,
    chr(0xF711): Key.F14,
    chr(0xF712): Key.F15,
    chr(0xF713): Key.F16,
    chr(0xF714): Key.F17,
    chr(0xF715): Key.F18,
    chr(0xF716): Key.F19,
    # chr(0xF717): Key.F20,
    chr(0xF729): Key.HOME,
    chr(0xF72B): Key.END,
    chr(0xF728): Key.DELETE,
    chr(0xF72C): Key.PAGE_UP,
    chr(0xF72D): Key.PAGE_DOWN,
    chr(0xF700): Key.UP,
    chr(0xF701): Key.DOWN,
    chr(0xF702): Key.LEFT,
    chr(0xF703): Key.RIGHT,
}

# Add in all the standard printable keys
KEY_CHARS_TO_TOGA = {
    key.value: key
    for key in Key
    if key.is_printable() and not key.value.startswith("numpad")
}
KEY_CHARS_TO_TOGA.update(NON_PRINTABLE_KEYS_TO_TOGA)

# Shifted punctuation on QWERTY keyboards
SHIFTED_KEY_CHARS = {
    "`": "~",
    "1": "!",
    "2": "@",
    "3": "#",
    "4": "$",
    "5": "%",
    "6": "^",
    "7": "&",
    "8": "*",
    "9": "(",
    "0": ")",
    "-": "_",
    "=": "+",
    "[": "{",
    "]": "}",
    ";": ":",
    "'": '"',
    "\\": "|",
    ",": "<",
    ".": ">",
    "/": "?",
    "§": "±",  # International English keyboards
}

# Numpad needs actual keys pressed to tell difference from other
# ways of getting the character.
NUMPAD_KEYCODES = {
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
}


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


def toga_key(event):
    """Convert a Cocoa NSKeyEvent into a Toga Key."""
    # In general, we can get something close to the Toga keys by using
    # charactersByApplyingModifiers with command or command-shift set
    #
    # Experimentation shows the following behaviour
    # - on English keyboards, command and command-shift give same key always
    # - on Latin alphabet keyboards, command uses native layout and
    #   command-shift gives shifted version of the key, if any
    # - on non-latin keyboards, command uses QWERTY layout and
    #   command-shift gives shifted version of the key
    #
    # This gives the following heuristic:
    # - special case numpad and non-printing characters
    # - look to see what character we get if just Command pressed
    # - if shift is down
    #   - see what we get if Command-shift pressed
    #   - if it is upper-case of unshifted key
    #     - add the shift modifier, use the original (lower-case) key
    #   - if shifted and unshifted are different
    #     - no shift modifier, but use the shifted key
    #   - if key is a punctuation key:
    #     - we're likely on an English keyboard, so use shifted QWERTY key
    #   - otherwise:
    #     - add the shift modifier and use the original key
    #
    # Numpad keys are not differentiated by charactersByApplyingModifiers,
    # so we'll handle them separately
    modifiers = set()

    if event.keyCode in NUMPAD_KEYCODES:
        toga_key = NUMPAD_KEYCODES[event.keyCode]
        if event.modifierFlags & NSEventModifierFlagShift:
            modifiers.add(Key.SHIFT)
    elif str(event.charactersIgnoringModifiers) in NON_PRINTABLE_KEYS_TO_TOGA:
        key = str(event.characters)
        toga_key = NON_PRINTABLE_KEYS_TO_TOGA[key]
        if event.modifierFlags & NSEventModifierFlagShift:
            modifiers.add(Key.SHIFT)
    else:
        key = str(event.charactersByApplyingModifiers(NSEventModifierFlagCommand))
        if event.modifierFlags & NSEventModifierFlagShift:
            shift_key = str(
                event.charactersByApplyingModifiers(
                    NSEventModifierFlagCommand | NSEventModifierFlagShift
                )
            )
            if shift_key != key:
                if shift_key == key.upper():  # pragma: no cover
                    # An English layout keyboard will never reach here
                    # so the tests currently don't exercise it
                    modifiers.add(Key.SHIFT)
                else:
                    key = shift_key
            elif key in SHIFTED_KEY_CHARS:
                # Likely English keyboard
                key = SHIFTED_KEY_CHARS[key]
            else:
                modifiers.add(Key.SHIFT)

        toga_key = KEY_CHARS_TO_TOGA.get(key)

    # Handle Modifiers
    if event.modifierFlags & NSEventModifierFlagCommand:
        modifiers.add(Key.MOD_1)
    if event.modifierFlags & NSEventModifierFlagOption:
        modifiers.add(Key.MOD_2)
    if event.modifierFlags & NSEventModifierFlagControl:
        modifiers.add(Key.MOD_3)

    return {"key": toga_key, "modifiers": modifiers}
