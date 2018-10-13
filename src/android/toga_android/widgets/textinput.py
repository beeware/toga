from android.view import Gravity

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
        self.interface.factory.not_implemented('TextInput.set_readonly()')

    def set_placeholder(self, value):
        self.native.setHint(value)

    def set_alignment(self, value):
        self.native.setGravity({
                LEFT_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.LEFT,
                RIGHT_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.RIGHT,
                CENTER_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                JUSTIFIED_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
                NATURAL_ALIGNED: Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL,
            }[value])

    def set_font(self, value):
        self.interface.factory.not_implemented('TextInput.set_font()')

    def get_value(self, value):
        return str(self.native.getText())

    def set_value(self, value):
        self.native.setText(value)

    def rehint(self):
        # Height of a text input is known and fixed.
        # print("REHINT text input", self, self.native.getMeasuredWidth(), self.native.getMeasuredHeight())
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.getMeasuredHeight() / self.app.native.device_scale

    def set_on_change(self, handler):
        # No special handling required.
        pass
