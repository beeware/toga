
class Variable(Source):
    """A value source that helps you to store and manage a single value value.

    Args:
        value: The value for the variable.
    """

    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._refresh()
