from .libs import Gdk

from toga.keys import Key

GDK_KEYS = {
    Gdk.KEY_Escape: Key.ESCAPE,

    Gdk.KEY_F1: Key.F1,
    Gdk.KEY_F2: Key.F2,
    Gdk.KEY_F3: Key.F3,
    Gdk.KEY_F4: Key.F4,
    Gdk.KEY_F5: Key.F5,
    Gdk.KEY_F6: Key.F6,
    Gdk.KEY_F7: Key.F7,
    Gdk.KEY_F8: Key.F8,
    Gdk.KEY_F9: Key.F9,
    Gdk.KEY_F10: Key.F10,
    Gdk.KEY_F11: Key.F11,
    Gdk.KEY_F12: Key.F12,
    Gdk.KEY_F13: Key.F13,
    Gdk.KEY_F14: Key.F14,
    Gdk.KEY_F15: Key.F15,
    Gdk.KEY_F16: Key.F16,
    Gdk.KEY_F17: Key.F17,
    Gdk.KEY_F18: Key.F18,
    Gdk.KEY_F19: Key.F19,

    Gdk.KEY_quoteleft: Key.BACK_QUOTE,

    Gdk.KEY_1: Key._1,
    Gdk.KEY_2: Key._2,
    Gdk.KEY_3: Key._3,
    Gdk.KEY_4: Key._4,
    Gdk.KEY_5: Key._5,
    Gdk.KEY_6: Key._6,
    Gdk.KEY_7: Key._7,
    Gdk.KEY_8: Key._8,
    Gdk.KEY_9: Key._9,
    Gdk.KEY_0: Key._0,

    Gdk.KEY_minus: Key.MINUS,
    Gdk.KEY_equal: Key.EQUAL,
    Gdk.KEY_BackSpace: Key.BACKSPACE,

    Gdk.KEY_asciitilde: Key.TILDE,
    Gdk.KEY_exclam: Key.EXCLAMATION,
    Gdk.KEY_at: Key.AT,
    Gdk.KEY_numbersign: Key.HASH,
    Gdk.KEY_dollar: Key.DOLLAR,
    Gdk.KEY_percent: Key.PERCENT,
    Gdk.KEY_asciicircum: Key.CARET,
    Gdk.KEY_ampersand: Key.AMPERSAND,
    Gdk.KEY_asterisk: Key.ASTERISK,
    Gdk.KEY_parenleft: Key.OPEN_PARENTHESIS,
    Gdk.KEY_parenright: Key.CLOSE_PARENTHESIS,
    Gdk.KEY_underscore: Key.UNDERSCORE,
    Gdk.KEY_plus: Key.PLUS,

    Gdk.KEY_a: Key.A,
    Gdk.KEY_b: Key.B,
    Gdk.KEY_c: Key.C,
    Gdk.KEY_d: Key.D,
    Gdk.KEY_e: Key.E,
    Gdk.KEY_f: Key.F,
    Gdk.KEY_g: Key.G,
    Gdk.KEY_h: Key.H,
    Gdk.KEY_i: Key.I,
    Gdk.KEY_j: Key.J,
    Gdk.KEY_k: Key.K,
    Gdk.KEY_l: Key.L,
    Gdk.KEY_m: Key.M,
    Gdk.KEY_n: Key.N,
    Gdk.KEY_o: Key.O,
    Gdk.KEY_p: Key.P,
    Gdk.KEY_q: Key.Q,
    Gdk.KEY_r: Key.R,
    Gdk.KEY_s: Key.S,
    Gdk.KEY_t: Key.T,
    Gdk.KEY_u: Key.U,
    Gdk.KEY_v: Key.V,
    Gdk.KEY_w: Key.W,
    Gdk.KEY_x: Key.X,
    Gdk.KEY_y: Key.Y,
    Gdk.KEY_z: Key.Z,

    Gdk.KEY_A: Key.A,
    Gdk.KEY_B: Key.B,
    Gdk.KEY_C: Key.C,
    Gdk.KEY_D: Key.D,
    Gdk.KEY_E: Key.E,
    Gdk.KEY_F: Key.F,
    Gdk.KEY_G: Key.G,
    Gdk.KEY_H: Key.H,
    Gdk.KEY_I: Key.I,
    Gdk.KEY_J: Key.J,
    Gdk.KEY_K: Key.K,
    Gdk.KEY_L: Key.L,
    Gdk.KEY_M: Key.M,
    Gdk.KEY_N: Key.N,
    Gdk.KEY_O: Key.O,
    Gdk.KEY_P: Key.P,
    Gdk.KEY_Q: Key.Q,
    Gdk.KEY_R: Key.R,
    Gdk.KEY_S: Key.S,
    Gdk.KEY_T: Key.T,
    Gdk.KEY_U: Key.U,
    Gdk.KEY_V: Key.V,
    Gdk.KEY_W: Key.W,
    Gdk.KEY_X: Key.X,
    Gdk.KEY_Y: Key.Y,
    Gdk.KEY_Z: Key.Z,

    Gdk.KEY_Tab: Key.TAB,
    Gdk.KEY_bracketleft: Key.OPEN_BRACKET,
    Gdk.KEY_bracketright: Key.CLOSE_BRACKET,
    Gdk.KEY_backslash: Key.BACKSLASH,

    Gdk.KEY_braceleft: Key.OPEN_BRACE,
    Gdk.KEY_braceright: Key.CLOSE_BRACE,
    Gdk.KEY_bar: Key.PIPE,

    Gdk.KEY_semicolon: Key.SEMICOLON,
    Gdk.KEY_apostrophe: Key.QUOTE,
    Gdk.KEY_Return: Key.ENTER,

    Gdk.KEY_colon: Key.COLON,
    Gdk.KEY_quotedbl: Key.DOUBLE_QUOTE,

    Gdk.KEY_comma: Key.COMMA,
    Gdk.KEY_period: Key.FULL_STOP,
    Gdk.KEY_slash: Key.SLASH,

    Gdk.KEY_less: Key.LESS_THAN,
    Gdk.KEY_greater: Key.GREATER_THAN,
    Gdk.KEY_question: Key.QUESTION,

    Gdk.KEY_Delete: Key.DELETE,
    Gdk.KEY_Home: Key.HOME,
    Gdk.KEY_End: Key.END,
    Gdk.KEY_Page_Up: Key.PAGE_UP,
    Gdk.KEY_Page_Down: Key.PAGE_DOWN,

    Gdk.KEY_Left: Key.LEFT,
    Gdk.KEY_Right: Key.RIGHT,
    Gdk.KEY_Up: Key.UP,
    Gdk.KEY_Down: Key.DOWN,
}


def gdk_key(event):
    """Convert a GDK Key Event into a Toga event."""
    try:
        key = GDK_KEYS[event.keyval]

        modifiers = set()

        if event.state & Gdk.ModifierType.LOCK_MASK:
            modifiers.add(Key.CAPSLOCK)
        if event.state & Gdk.ModifierType.SHIFT_MASK:
            modifiers.add(Key.SHIFT)
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            modifiers.add(Key.CONTROL)
        if event.state & Gdk.ModifierType.META_MASK:
            modifiers.add(Key.OPTION)
        if event.state & Gdk.ModifierType.HYPER_MASK:
            modifiers.add(Key.COMMAND)

        return {
            'key': key,
            'modifiers': modifiers
        }
    except KeyError:
        return None
