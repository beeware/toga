from __future__ import annotations

from enum import Enum


class Key(Enum):
    """An enumeration providing a symbolic representation for the characters on
    a keyboard."""

    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"  # noqa: E741
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"  # noqa: E741
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"

    _0 = "0"
    _1 = "1"
    _2 = "2"
    _3 = "3"
    _4 = "4"
    _5 = "5"
    _6 = "6"
    _7 = "7"
    _8 = "8"
    _9 = "9"

    EXCLAMATION = "!"
    AT = "@"
    HASH = "#"
    DOLLAR = "$"
    PERCENT = "%"
    CARET = "^"
    AMPERSAND = "&"
    ASTERISK = "*"
    OPEN_PARENTHESIS = "("
    CLOSE_PARENTHESIS = ")"

    MINUS = "-"
    UNDERSCORE = "_"
    EQUAL = "="
    PLUS = "+"
    OPEN_BRACKET = "["
    CLOSE_BRACKET = "]"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    BACKSLASH = "\\"
    PIPE = "|"
    SEMICOLON = ";"
    COLON = ":"

    QUOTE = "'"
    DOUBLE_QUOTE = '"'
    COMMA = ","
    LESS_THAN = "<"
    FULL_STOP = "."
    GREATER_THAN = ">"
    SLASH = "/"
    QUESTION = "?"
    BACK_QUOTE = "`"
    TILDE = "~"

    ESCAPE = "<esc>"
    TAB = "<tab>"
    SPACE = " "

    BACKSPACE = "<backspace>"
    ENTER = "<enter>"

    CAPSLOCK = "<caps lock>"
    SHIFT = "<shift>"

    # Modifiers keys are handled slightly different on every platform
    # However, there is a broad platform-specific precedence for them.
    # Preserve the platform precedence behind generic naming.
    MOD_1 = "<mod 1>"  # CMD on macOS, CTRL on Linux/Windows
    MOD_2 = "<mod 2>"  # OPT on macOS, ALT on Linux/Windows
    MOD_3 = "<mod 3>"  # CTRL on macOS, Flag on Windows, Tux on Linux

    F1 = "<f1>"
    F2 = "<f2>"
    F3 = "<f3>"
    F4 = "<f4>"
    F5 = "<f5>"
    F6 = "<f6>"
    F7 = "<f7>"
    F8 = "<f8>"
    F9 = "<f9>"
    F10 = "<f10>"
    F11 = "<f11>"
    F12 = "<f12>"
    F13 = "<f13>"
    F14 = "<f14>"
    F15 = "<f15>"
    F16 = "<f16>"
    F17 = "<f17>"
    F18 = "<f18>"
    F19 = "<f19>"

    EJECT = "<eject>"

    HOME = "<home>"
    END = "<end>"
    INSERT = "<insert>"
    DELETE = "<delete>"
    PAGE_UP = "<pg up>"
    PAGE_DOWN = "<pg dn>"

    UP = "<up>"
    DOWN = "<down>"
    LEFT = "<left>"
    RIGHT = "<right>"

    NUMLOCK = "<num lock>"
    NUMPAD_0 = "numpad:0"
    NUMPAD_1 = "numpad:1"
    NUMPAD_2 = "numpad:2"
    NUMPAD_3 = "numpad:3"
    NUMPAD_4 = "numpad:4"
    NUMPAD_5 = "numpad:5"
    NUMPAD_6 = "numpad:6"
    NUMPAD_7 = "numpad:7"
    NUMPAD_8 = "numpad:8"
    NUMPAD_9 = "numpad:9"
    NUMPAD_CLEAR = "numpad:clear"
    NUMPAD_DECIMAL_POINT = "numpad:."
    NUMPAD_DIVIDE = "numpad:/"
    NUMPAD_ENTER = "numpad:enter"
    NUMPAD_EQUAL = "numpad:="
    NUMPAD_MINUS = "numpad:-"
    NUMPAD_MULTIPLY = "numpad:*"
    NUMPAD_PLUS = "numpad:+"

    SCROLLLOCK = "<scroll lock>"
    BEGIN = "<begin>"
    MENU = "<menu>"
    PAUSE = "<pause>"

    def is_printable(self) -> bool:
        """Does pressing the key result in a printable character?"""
        return not (self.value.startswith("<") and self.value.endswith(">"))

    def __add__(self, other: Key | str) -> str:
        """Allow two Keys to be concatenated, or a string to be concatenated to a Key.

        Produces a single string definition.

        e.g.,
        ``Toga.Key.MOD_1 + 'a'`` -> ``"<mod 1>a"``
        ``Toga.Key.MOD_1 + Toga.Key.SHIFT + 'a'`` -> ``"<mod 1><shift>a"``
        """
        try:
            # Try Key + Key
            return self.value + other.value
        except AttributeError:
            return self.value + other

    def __radd__(self, other: str) -> str:
        """Same as add."""
        return other + self.value
