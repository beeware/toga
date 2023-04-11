from travertino.size import at_least

from toga.constants import LEFT

from ..libs.android.text import InputType, TextWatcher
from ..libs.android.view import Gravity
from ..libs.android.widget import EditText
from .base import align
from .label import TextViewWidget


class TogaTextWatcher(TextWatcher):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
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
        self._textChangedListener = None
        self.native = EditText(self._native_activity)
        self.native.setInputType(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE
        )
        # Set default alignment
        self.set_alignment(LEFT)
        self.cache_textview_defaults()

    def get_value(self):
        return self.native.getText().toString()

    def set_readonly(self, value):
        self.native.setFocusable(not value)

    def set_placeholder(self, value):
        # Android EditText's setHint() requires a Python string.
        self.native.setHint(value if value is not None else "")

    def set_alignment(self, value):
        self.native.setGravity(Gravity.TOP | align(value))

    def set_value(self, value):
        self.native.setText(value)

    def set_on_change(self, handler):
        if self._textChangedListener:
            self.native.removeTextChangedListener(self._textChangedListener)
        self._textChangedListener = TogaTextWatcher(self)
        self.native.addTextChangedListener(self._textChangedListener)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        last_line = (self.native.getLineCount() - 1) * self.native.getLineHeight()
        self.native.scrollTo(0, last_line)

    def scroll_to_top(self):
        self.native.scrollTo(0, 0)
