from travertino.size import at_least

from ..libs.android.text import InputType
from ..libs.android.view import Gravity
from .textinput import TextInput


class MultilineTextInput(TextInput):
    def create(self):
        super().create(
            input_type=InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE,
            handle_confirm=False,
            handle_focus=False,
        )

    def set_alignment(self, value):
        self.set_textview_alignment(value, Gravity.TOP)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        self.native.setSelection(self.native.length())

    def scroll_to_top(self):
        self.native.setSelection(0)
