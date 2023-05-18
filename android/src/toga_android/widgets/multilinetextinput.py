from travertino.size import at_least

from toga.constants import LEFT

from ..libs.android.text import InputType, TextWatcher
from ..libs.android.view import Gravity
from ..libs.android.widget import EditText
from .label import TextViewWidget


class TogaTextWatcher(TextWatcher):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface

    def beforeTextChanged(self, _charSequence, _start, _count, _after):
        pass

    def afterTextChanged(self, _editable):
        if self.interface.on_change:
            self.interface.on_change(widget=self.interface)

    def onTextChanged(self, _charSequence, _start, _before, _count):
        pass


class MultilineTextInput(TextViewWidget):
    def create(self):
        self.native = EditText(self._native_activity)
        self.native.setInputType(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE
        )
        self.set_alignment(LEFT)
        self.native.addTextChangedListener(TogaTextWatcher(self))
        self.cache_textview_defaults()

    def get_value(self):
        return str(self.native.getText())

    def set_value(self, value):
        self.native.setText(value)

    def get_readonly(self):
        return not self.native.isFocusable()

    def set_readonly(self, readonly):
        if readonly:
            # Implicitly calls setFocusableInTouchMode(False)
            self.native.setFocusable(False)
        else:
            # Implicitly calls setFocusable(True)
            self.native.setFocusableInTouchMode(True)

    def get_placeholder(self):
        return str(self.native.getHint())

    def set_placeholder(self, value):
        self.native.setHint(value)

    def set_alignment(self, value):
        self.set_textview_alignment(value, Gravity.TOP)

    def set_background_color(self, value):
        self.set_background_color_tint(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        self.native.scrollTo(0, self.native.getLayout().getHeight())

    def scroll_to_top(self):
        self.native.scrollTo(0, 0)
