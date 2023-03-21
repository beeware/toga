from travertino.size import at_least

from ..libs.android.text import InputType, TextWatcher
from ..libs.android.view import Gravity, View__MeasureSpec
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


class TextInput(TextViewWidget):
    def create(self):
        self._textChangedListener = None
        self.native = EditText(self._native_activity)
        self.native.setInputType(InputType.TYPE_CLASS_TEXT)
        self.cache_textview_defaults()

    def get_value(self):
        return self.native.getText().toString()

    def set_readonly(self, value):
        self.native.setFocusable(not value)

    def set_placeholder(self, value):
        # Android EditText's setHint() requires a Python string.
        self.native.setHint(value if value is not None else "")

    def set_alignment(self, value):
        # Refuse to set alignment unless widget has been added to a container.
        # This is because Android EditText requires LayoutParams before
        # setGravity() can be called.
        if not self.native.getLayoutParams():
            return
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))

    def set_value(self, value):
        self.native.setText(value)

    def set_on_change(self, handler):
        if self._textChangedListener:
            self.native.removeTextChangedListener(self._textChangedListener)
        self._textChangedListener = TogaTextWatcher(self)
        self.native.addTextChangedListener(self._textChangedListener)

    def set_error(self, error_message):
        self.interface.factory.not_implemented("TextInput.set_error()")

    def clear_error(self):
        self.interface.factory.not_implemented("TextInput.clear_error()")

    def is_valid(self):
        self.interface.factory.not_implemented("TextInput.is_valid()")

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        # Refuse to call measure() if widget has no container, i.e., has no LayoutParams.
        # On Android, EditText's measure() throws NullPointerException if the widget has no
        # LayoutParams.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_on_gain_focus(self, handler):
        self.interface.factory.not_implemented("TextInput.set_on_gain_focus()")

    def set_on_lose_focus(self, handler):
        self.interface.factory.not_implemented("TextInput.set_on_lose_focus()")
