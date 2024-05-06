from toga.keys import Key

from .libs import Gdk

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
    Gdk.KEY_Caps_Lock: Key.CAPSLOCK,
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
    Gdk.KEY_space: Key.SPACE,
    Gdk.KEY_colon: Key.COLON,
    Gdk.KEY_quotedbl: Key.DOUBLE_QUOTE,
    Gdk.KEY_comma: Key.COMMA,
    Gdk.KEY_period: Key.FULL_STOP,
    Gdk.KEY_slash: Key.SLASH,
    Gdk.KEY_less: Key.LESS_THAN,
    Gdk.KEY_greater: Key.GREATER_THAN,
    Gdk.KEY_question: Key.QUESTION,
    Gdk.KEY_Insert: Key.INSERT,
    Gdk.KEY_Delete: Key.DELETE,
    Gdk.KEY_Begin: Key.BEGIN,
    Gdk.KEY_Menu: Key.MENU,
    Gdk.KEY_Home: Key.HOME,
    Gdk.KEY_End: Key.END,
    Gdk.KEY_Page_Up: Key.PAGE_UP,
    Gdk.KEY_Page_Down: Key.PAGE_DOWN,
    Gdk.KEY_Left: Key.LEFT,
    Gdk.KEY_Right: Key.RIGHT,
    Gdk.KEY_Up: Key.UP,
    Gdk.KEY_Down: Key.DOWN,
    Gdk.KEY_Num_Lock: Key.NUMLOCK,
    Gdk.KEY_KP_Enter: Key.NUMPAD_ENTER,
    Gdk.KEY_KP_0: Key.NUMPAD_0,
    Gdk.KEY_KP_1: Key.NUMPAD_1,
    Gdk.KEY_KP_2: Key.NUMPAD_2,
    Gdk.KEY_KP_3: Key.NUMPAD_3,
    Gdk.KEY_KP_4: Key.NUMPAD_4,
    Gdk.KEY_KP_5: Key.NUMPAD_5,
    Gdk.KEY_KP_6: Key.NUMPAD_6,
    Gdk.KEY_KP_7: Key.NUMPAD_7,
    Gdk.KEY_KP_8: Key.NUMPAD_8,
    Gdk.KEY_KP_9: Key.NUMPAD_9,
    Gdk.KEY_KP_Home: Key.HOME,
    Gdk.KEY_KP_End: Key.END,
    Gdk.KEY_KP_Page_Down: Key.PAGE_DOWN,
    Gdk.KEY_KP_Page_Up: Key.PAGE_UP,
    Gdk.KEY_KP_Left: Key.LEFT,
    Gdk.KEY_KP_Right: Key.RIGHT,
    Gdk.KEY_KP_Up: Key.UP,
    Gdk.KEY_KP_Down: Key.DOWN,
    Gdk.KEY_KP_Delete: Key.DELETE,
    Gdk.KEY_KP_Insert: Key.INSERT,
    Gdk.KEY_KP_Add: Key.NUMPAD_PLUS,
    Gdk.KEY_KP_Subtract: Key.NUMPAD_MINUS,
    Gdk.KEY_KP_Multiply: Key.NUMPAD_MULTIPLY,
    Gdk.KEY_KP_Divide: Key.NUMPAD_DIVIDE,
    Gdk.KEY_KP_Begin: Key.BEGIN,
    Gdk.KEY_Pause: Key.PAUSE,
    Gdk.KEY_ISO_Left_Tab: Key.TAB,
    Gdk.KEY_Scroll_Lock: Key.SCROLLLOCK,
    Gdk.KEY_Shift_L: Key.SHIFT,
    Gdk.KEY_Shift_R: Key.SHIFT,
    Gdk.KEY_Control_L: Key.MOD_1,
    Gdk.KEY_Control_R: Key.MOD_1,
    Gdk.KEY_Alt_L: Key.MOD_2,
    Gdk.KEY_Alt_R: Key.MOD_2,
    Gdk.KEY_Hyper_L: Key.MOD_3,
    Gdk.KEY_Hyper_R: Key.MOD_3,
}

GTK_KEY_NAMES = {
    toga_keyval: Gdk.keyval_name(gdk_keyval)
    for gdk_keyval, toga_keyval in GDK_KEYS.items()
}

GTK_MODIFIER_CODES = {
    Key.SHIFT: "<Shift>",
    Key.MOD_1: "<Primary>",
    Key.MOD_2: "<Alt>",
    Key.MOD_3: "<Hyper>",
}


def toga_key(event):
    """Convert a GDK Key Event into a Toga key."""
    try:
        key = GDK_KEYS[event.keyval]
    except KeyError:  # pragma: no cover
        # Ignore any key event code we can't map. This can happen for weird key
        # combination (ctrl-alt-tux), and if the X server has weird key
        # bindings. If we can't map it, we can't really type it either, so we
        # need to no-cover this branch.
        return None

    modifiers = set()

    if event.state & Gdk.ModifierType.SHIFT_MASK:
        modifiers.add(Key.SHIFT)
    if event.state & Gdk.ModifierType.CONTROL_MASK:
        modifiers.add(Key.MOD_1)
    if event.state & Gdk.ModifierType.META_MASK:
        modifiers.add(Key.MOD_2)
    if event.state & Gdk.ModifierType.HYPER_MASK:
        modifiers.add(Key.MOD_3)

    return {"key": key, "modifiers": modifiers}


def gtk_accel(shortcut):
    """Convert a Toga shortcut definition into GTK accelerator definition."""
    accel = shortcut
    # Convert the shortcut into string form.
    try:
        accel = shortcut.value
    except AttributeError:
        accel = shortcut

    modifiers = []
    # Remove any modifiers from the shortcut definition
    for key, code in GTK_MODIFIER_CODES.items():
        if key.value in accel:
            accel = accel.replace(key.value, "")
            modifiers.append(code)

    # If the accelerator text is upper case, add a shift modifier.
    if accel.isalpha() and accel.isupper():
        accel = accel.lower()
        modifiers.append("<Shift>")

    # Find the canonical definition of the remaining key.
    for key, code in GTK_KEY_NAMES.items():
        if key.value == accel:
            accel = accel.replace(key.value, code)

    accel = "".join(modifiers) + accel
    return accel
