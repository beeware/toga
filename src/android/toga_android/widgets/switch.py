from travertino.size import at_least

from .base import Widget
from ..libs import android_widgets


class OnCheckedChangeListener(android_widgets.CompoundButton__OnCheckedChangeListener):
    def __init__(self, impl):
        super().__init__()
        self._impl = impl

    def onCheckedChanged(self, _button, _checked):
        if self._impl.interface.on_toggle:
            self._impl.interface.on_toggle(widget=self._impl.interface)


class Switch(Widget):
    def create(self):
        self.native = android_widgets.Switch(self._native_activity)
        self.native.setOnCheckedChangeListener(OnCheckedChangeListener(self))

    def set_label(self, label):
        # When changing the text, Android needs a `setSingleLine(False)` call in order
        # to be willing to recompute the width of the text. Without the call, it will
        # constrain the new text to have the same line width as the old text, resulting
        # in unnecessary creation of new lines. In other words, `setSingleLine(False)`
        # is required to get the text to truly **use** one single line!
        self.native.setSingleLine(False)
        self.native.setText(str(self.interface.label))
        self.rehint()

    def set_is_on(self, value):
        self.native.setChecked(bool(value))

    def get_is_on(self):
        return self.native.isChecked()

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self.native.setTextSize(android_widgets.TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self.native.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def set_on_toggle(self, handler):
        # No special handling required
        pass

    def rehint(self):
        if self.native.getLayoutParams() is None:
            return
        self.native.measure(
            android_widgets.View__MeasureSpec.UNSPECIFIED, android_widgets.View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
