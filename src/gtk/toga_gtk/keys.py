from toga.keys import Key

_KEY_MAP = {
    0xFF51: Key.LEFT,
    0xFF52: Key.UP,
    0xFF53: Key.RIGHT,
    0xFF54: Key.DOWN,
}


def gtk_to_key(key):
    return _KEY_MAP.get(key)
