from .base import Widget


class TextInput(Widget):
    def __html__(self):
        return """
            <input id="toga_{id}" class="toga input btn-block" style="{style}" value="{value}">
        """.format(
            id=self.interface.id,
            style=self.interface.style.__css__(),
            value=self.interface.value,
        )

    def create(self):
        pass

    def set_readonly(self, value):
        pass

    def set_placeholder(self, value):
        pass

    def get_value(self):
        print(f"client get value")
        if self.native:
            return self.native.value
        else:
            return ''

    def set_value(self, value):
        if self.native:
            print(f"client set value {value!r}")
            self.native.value = value
        else:
            print(f"set value {value!r}")

    def set_font(self, font):
        pass

    def set_alignment(self, value):
        pass

    def rehint(self):
        pass

    def set_on_change(self, handler):
        pass

    def set_on_gain_focus(self, handler):
        pass

    def set_on_lose_focus(self, handler):
        pass

    def set_error(self, error_message):
        pass

    def clear_error(self):
        pass
