from enum import Enum


class Key(Enum):
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'

    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '9'

    EXCLAMATION = '!'
    AT = '@'
    HASH = '#'
    DOLLAR = '$'
    PERCENT = '%'
    CARET = '^'
    AMPERSAND = '&'
    ASTERISK = '*'
    OPEN_PARENTHESIS = '('
    CLOSE_PARENTHESIS = ')'

    MINUS = '-'
    UNDERSCORE = '_'
    EQUAL = '='
    PLUS = '+'
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
    OPEN_BRACE = '{'
    CLOSE_BRACE = '}'
    BACKSLASH = '\\'
    PIPE = '|'
    SEMICOLON = ';'
    COLON = ':'

    QUOTE = '\''
    DOUBLE_QUOTE = '"'
    COMMA = ','
    LESS_THAN = '<'
    FULL_STOP = '.'
    GREATER_THAN = '>'
    SLASH = '/'
    QUESTION = '?'
    BACK_QUOTE = '`'
    TILDE = '~'

    ESCAPE = '<esc>'
    TAB = '<tab>'
    SPACE = ' '

    BACKSPACE = '<backspace>'
    ENTER = '<enter>'

    CAPSLOCK = '<caps lock>'
    SHIFT = '<shift>'

    # Modifiers keys are handled slightly different on every platform
    # However, there is a broad platform-specific precedence for them.
    # Preserve the platform precedence behind generic naming.
    MOD_1 = '<mod 1>'  # CMD on macOS, CTRL on Linux/Windows
    MOD_2 = '<mod 2>'  # OPT on macOS, ALT on Linux/Windows
    MOD_3 = '<mod 3>'  # CTRL on macOs, Flag on Windows, Tux on Linux

    F1 = '<F1>'
    F2 = '<F2>'
    F3 = '<F3>'
    F4 = '<F4>'
    F5 = '<F5>'
    F6 = '<F6>'
    F7 = '<F7>'
    F8 = '<F8>'
    F9 = '<F9>'
    F10 = '<F10>'
    F11 = '<F11>'
    F12 = '<F12>'
    F13 = '<F13>'
    F14 = '<F14>'
    F15 = '<F15>'
    F16 = '<F16>'
    F17 = '<F17>'
    F18 = '<F18>'
    F19 = '<F19>'

    EJECT = '<eject>'

    HOME = '<home>'
    END = '<end>'
    DELETE = '<delete>'
    PAGE_UP = '<pg up>'
    PAGE_DOWN = '<pg dn>'

    UP = '<up>'
    DOWN = '<down>'
    LEFT = '<left>'
    RIGHT = '<right>'

    NUMPAD_0 = 'numpad:0'
    NUMPAD_1 = 'numpad:1'
    NUMPAD_2 = 'numpad:2'
    NUMPAD_3 = 'numpad:3'
    NUMPAD_4 = 'numpad:4'
    NUMPAD_5 = 'numpad:5'
    NUMPAD_6 = 'numpad:6'
    NUMPAD_7 = 'numpad:7'
    NUMPAD_8 = 'numpad:8'
    NUMPAD_9 = 'numpad:9'
    NUMPAD_CLEAR = 'numpad:clear'
    NUMPAD_DECIMAL_POINT = 'numpad:.'
    NUMPAD_DIVIDE = 'numpad:/'
    NUMPAD_ENTER = 'numpad:enter'
    NUMPAD_EQUAL = 'numpad:='
    NUMPAD_MINUS = 'numpad:-'
    NUMPAD_MULTIPLY = 'numpad:*'
    NUMPAD_PLUS = 'numpad:+'

    def is_printable(self):
        return not (self.value.startswith('<') and self.value.endswith('>'))

    def __add__(self, other):
        """Allow two Keys to be concatenated, or a string to be concatenated
        to a Key.

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
