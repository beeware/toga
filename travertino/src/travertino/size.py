class at_least:
    """An annotation to wrap around a value to describe that it is a minimum bound"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"at least {self.value}"

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False


class BaseIntrinsicSize:
    """Representation of the intrinsic size of an object.

    width: The width of the node.
    height: The height of the node.
    """

    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def __repr__(self):
        return f"({self.width}, {self.height})"
