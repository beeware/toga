__all__ = ["Enum", "auto"]


class Enum:
    pass


_next_auto = 0


def auto():
    global _next_auto
    _next_auto += 1
    return _next_auto
