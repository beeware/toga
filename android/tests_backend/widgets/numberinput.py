import pytest

from .textinput import TextInputProbe


class NumberInputProbe(TextInputProbe):
    allows_invalid_value = False
    allows_empty_value = True
    allows_extra_digits = True

    @property
    def value(self):
        return str(self.native.getText())

    def clear_input(self):
        self.native.setText("")

    async def increment(self):
        pytest.xfail("This backend doesn't support stepped increments")

    async def decrement(self):
        pytest.xfail("This backend doesn't support stepped increments")

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
