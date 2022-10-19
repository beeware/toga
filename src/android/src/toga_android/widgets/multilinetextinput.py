from toga.constants import LEFT
from travertino.size import at_least

from toga_android.colors import native_color

from ..libs.android.text import InputType, TextWatcher
from ..libs.android.util import TypedValue
from ..libs.android.view import Gravity
from ..libs.android.widget import EditText
from .base import Widget, align


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


class MultilineTextInput(Widget):
    def create(self):
        self._textChangedListener = None
        self.native = EditText(self._native_activity)
        self.native.setInputType(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE
        )
        # Set default alignment
        self.set_alignment(LEFT)

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
        self.native.setGravity(Gravity.TOP | align(value))

    def set_color(self, color):
        if color:
            self.native.setTextColor(native_color(color))

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self.native.setTextSize(TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self.native.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def set_value(self, value):
        self.native.setText(value)

    def set_on_change(self, handler):
        if self._textChangedListener:
            self.native.removeTextChangedListener(self._textChangedListener)
        self._textChangedListener = TogaTextWatcher(self)
        self.native.addTextChangedListener(self._textChangedListener)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
