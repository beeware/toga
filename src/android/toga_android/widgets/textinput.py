from travertino.size import at_least

from .base import Widget


class TogaTextInput(extends=android.widget.EditText):
    @super({context: android.content.Context})
    def __init__(self, context, interface):
        self.interface = interface


class TextInput(Widget):
    def create(self):
        self.native = TogaTextInput(self.app.native, self.interface)

    def set_readonly(self, value):
        # self.native.editable = not value
        pass

    def set_placeholder(self, value):
        # self.native.cell.placeholderString = self._placeholder
        pass

    def set_alignment(self, value):
        pass

    def set_font(self, value):
        pass

    def get_value(self, value):
        raise NotImplementedError()

    def set_value(self, value):
        self.native.setText(value)

    def rehint(self):
        # Height of a text input is known and fixed.
        # print("REHINT text input", self, self.native.getMeasuredWidth(), self.native.getMeasuredHeight())
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.getMeasuredHeight() / self.app.native.device_scale

    def set_on_change(self, handler):
        pass
