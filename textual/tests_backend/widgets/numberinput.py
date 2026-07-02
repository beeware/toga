from decimal import Decimal

from toga.widgets.numberinput import _clean_decimal_str

from .textinput import TextInputProbe


class NumberInputProbe(TextInputProbe):
    allows_invalid_value = False
    allows_empty_value = True
    allows_extra_digits = True
    allows_unchanged_updates = True

    def clear_input(self):
        self.native._reactive_value = ""
        self.impl.on_input_changed()

    async def increment(self):
        self.widget.value = (self.widget.value or Decimal(0)) + self.widget.step

    async def decrement(self):
        self.widget.value = (self.widget.value or Decimal(0)) - self.widget.step

    async def type_character(self, char):
        if self.widget.readonly:
            return

        if char == "<backspace>":
            new_value = self.native.value[:-1]
        elif char in {"\n", "<esc>"}:
            return
        else:
            new_value = f"{self.native.value}{char}"

        clean_value = _clean_decimal_str(new_value)
        if clean_value != new_value:
            return

        self.native._reactive_value = clean_value
        self.impl.on_input_changed()
