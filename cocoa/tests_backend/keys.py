from rubicon.objc import NSPoint

from toga import Key
from toga_cocoa.keys import COCOA_KEY_CODES, COCOA_MODIFIERS
from toga_cocoa.libs import (
    NSEvent,
    NSEventType,
)

# A map of toga key codes to physical keys of a US keyboard
# These are derived from the old Apple Extended Keyboard's internal codes,
# and represent physical keys. The mapping is to typical US/International
# English key layouts; different key layouts will associate the same key
# codes with different characters (eg. on an AZERTY layout, key code 12 is 'A')
# For a comprehensive list see:
# https://macbiblioblog.blogspot.com/2014/12/key-codes-for-function-and-special-keys.html
KEY_CODES = {
    Key.A.value: 0,
    Key.S.value: 1,
    Key.D.value: 2,
    Key.F.value: 3,
    Key.H.value: 4,
    Key.G.value: 5,
    Key.Z.value: 6,
    Key.X.value: 7,
    Key.C.value: 8,
    Key.V.value: 9,
    # Key.SECTION.value: 10,  # UK/International English
    Key.B.value: 11,
    Key.Q.value: 12,
    Key.W.value: 13,
    Key.E.value: 14,
    Key.R.value: 15,
    Key.Y.value: 16,
    Key.T.value: 17,
    Key._1.value: 18,
    Key._2.value: 19,
    Key._3.value: 20,
    Key._4.value: 21,
    Key._6.value: 22,
    Key._5.value: 23,
    Key.EQUAL.value: 24,
    Key._9.value: 25,
    Key._7.value: 26,
    Key.MINUS.value: 27,
    Key._8.value: 28,
    Key._0.value: 29,
    Key.CLOSE_BRACKET.value: 30,
    Key.O.value: 31,
    Key.U.value: 32,
    Key.OPEN_BRACKET.value: 33,
    Key.I.value: 34,
    Key.P.value: 35,
    Key.ENTER.value: 36,
    Key.L.value: 37,
    Key.J.value: 38,
    Key.QUOTE.value: 39,
    Key.K.value: 40,
    Key.SEMICOLON.value: 41,
    Key.BACKSLASH.value: 42,
    Key.COMMA.value: 43,
    Key.SLASH.value: 44,
    Key.N.value: 45,
    Key.M.value: 46,
    Key.FULL_STOP.value: 47,
    Key.TAB.value: 48,
    Key.SPACE.value: 49,
    Key.BACK_QUOTE.value: 50,
    Key.BACKSPACE.value: 51,
    # Key.LINEFEED.value: 52,
    Key.ESCAPE.value: 53,
    # 54
    Key.MOD_1.value: 55,
    Key.SHIFT.value: 56,
    Key.CAPSLOCK.value: 57,
    Key.MOD_2.value: 58,
    Key.MOD_3.value: 59,
    # Key.RIGHT_SHIFT.value: 60,
    # Key.RIGHT_OPTION.value: 61,
    # Key.RIGHT_CONTROL.value: 62,
    # Key.FUNCTION.value: 63,
    Key.F17.value: 64,
    Key.NUMPAD_DECIMAL_POINT.value: 65,
    # 66
    Key.NUMPAD_MULTIPLY.value: 67,
    # 68
    Key.NUMPAD_PLUS.value: 69,
    # 70
    Key.NUMPAD_CLEAR.value: 71,
    # Key.VOLUME_UP.value: 72,
    # Key.VOLUME_DOWN.value: 73,
    # Key.MUTE.value: 74,
    Key.NUMPAD_DIVIDE.value: 75,
    Key.NUMPAD_ENTER.value: 76,
    # 77
    Key.NUMPAD_MINUS.value: 78,
    Key.F18.value: 79,
    Key.F19.value: 80,
    Key.NUMPAD_EQUAL.value: 81,
    Key.NUMPAD_0.value: 82,
    Key.NUMPAD_1.value: 83,
    Key.NUMPAD_2.value: 84,
    Key.NUMPAD_3.value: 85,
    Key.NUMPAD_4.value: 86,
    Key.NUMPAD_5.value: 87,
    Key.NUMPAD_6.value: 88,
    Key.NUMPAD_7.value: 89,
    # Key.F20.value: 90,
    Key.NUMPAD_8.value: 91,
    Key.NUMPAD_9.value: 92,
    Key.F5.value: 96,
    Key.F6.value: 97,
    Key.F7.value: 98,
    Key.F3.value: 99,
    Key.F8.value: 100,
    Key.F9.value: 101,
    # 102
    Key.F11.value: 103,
    # 104
    Key.F13.value: 105,
    Key.F16.value: 106,
    Key.F14.value: 107,
    Key.F10.value: 109,
    # 110
    Key.F12.value: 111,
    # 112
    Key.F14.value: 113,
    # 114.value: Key.HELP / Key.INSERT
    Key.HOME.value: 115,
    Key.PAGE_UP.value: 116,
    Key.DELETE.value: 117,
    Key.F4.value: 118,
    Key.END.value: 119,
    Key.F2.value: 120,
    Key.PAGE_DOWN.value: 121,
    Key.F1.value: 122,
    Key.LEFT.value: 123,
    Key.RIGHT.value: 124,
    Key.DOWN.value: 125,
    Key.UP.value: 126,
}

SHIFT_KEY_CODES = {
    # Key.PLUS_MINUS.value: 10,  # UK/International English
    Key.EXCLAMATION.value: 18,
    Key.AT.value: 19,
    Key.HASH.value: 20,
    Key.DOLLAR.value: 21,
    Key.PERCENT.value: 22,
    Key.CARET.value: 23,
    Key.PLUS.value: 24,
    Key.OPEN_PARENTHESIS.value: 25,
    Key.AMPERSAND.value: 26,
    Key.UNDERSCORE.value: 27,
    Key.ASTERISK.value: 28,
    Key.CLOSE_PARENTHESIS.value: 29,
    Key.CLOSE_BRACE.value: 30,
    Key.OPEN_BRACE.value: 33,
    Key.DOUBLE_QUOTE.value: 39,
    Key.COLON.value: 41,
    Key.PIPE.value: 42,
    Key.LESS_THAN.value: 43,
    Key.QUESTION.value: 44,
    Key.GREATER_THAN.value: 47,
    Key.TILDE.value: 50,
}


def get_key_and_modifiers(combination) -> tuple[str, str, int, int]:
    """Given a key combination, return the key info and modifiers."""
    if isinstance(combination, Key):
        combination = combination.value

    # get modifiers
    modifiers = 0
    for modifier in COCOA_MODIFIERS:
        if modifier.value in combination:
            modifiers |= COCOA_MODIFIERS[modifier]
            combination = combination.replace(modifier.value, "")

    # get the characters and characters ignoring modifiers
    # this is simplified in that it doesn't apply effects of option or control
    # eg. on an English keyboard layout Option-A should be "å"
    key = combination
    for code, equiv in COCOA_KEY_CODES.items():
        key = key.replace(code.value, equiv)
    key_ignoring = key

    if combination.isupper():
        key = key.lower()
        key_code = KEY_CODES[combination.lower()]
        modifiers |= COCOA_MODIFIERS[Key.SHIFT]
    elif combination in KEY_CODES:
        key_code = KEY_CODES[combination]
    elif combination in SHIFT_KEY_CODES:
        key_code = SHIFT_KEY_CODES[combination]
        modifiers |= COCOA_MODIFIERS[Key.SHIFT]
    else:
        raise ValueError(f"Unknown key combination {combination}.")

    return key, key_ignoring, key_code, modifiers


def create_key_event(app, combination):
    """Create a key event for the app and key combination."""
    key, key_ignoring, key_code, modifiers = get_key_and_modifiers(combination)
    return NSEvent.keyEventWithType(
        NSEventType.KeyDown,
        location=NSPoint(0, 0),  # key presses don't have a location.
        modifierFlags=modifiers,
        timestamp=0,
        windowNumber=app.main_window._impl.native.windowNumber,
        context=None,
        characters=key,
        charactersIgnoringModifiers=key_ignoring,
        isARepeat=False,
        keyCode=key_code,
    )
