from android.text import InputType
from android.view import Gravity
from travertino.size import at_least

from .textinput import TextInput


class MultilineTextInput(TextInput):
    def create(self):
        super().create(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE,
        )

    def _on_change(self):
        self.interface.on_change()

    def _on_confirm(self):  # pragma: nocover
        pass  # The interface doesn't support this event.

    def _on_gain_focus(self):
        pass  # The interface doesn't support this event.

    def _on_lose_focus(self):
        pass  # The interface doesn't support this event.

    def set_alignment(self, value):
        self.set_textview_alignment(value, Gravity.TOP)

    # This method is necessary to override the TextInput base class.
    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        self.native.setSelection(self.native.length())

    def scroll_to_top(self):
        self.native.setSelection(0)
