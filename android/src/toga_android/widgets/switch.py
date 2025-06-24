from decimal import ROUND_UP

from android.view import View
from android.widget import CompoundButton, Switch as A_Switch
from java import dynamic_proxy
from travertino.size import at_least

from toga_android.widgets.base import ContainedWidget

from .label import TextViewWidget


class OnCheckedChangeListener(dynamic_proxy(CompoundButton.OnCheckedChangeListener)):
    def __init__(self, impl):
        super().__init__()
        self._impl = impl

    def onCheckedChanged(self, _button, _checked):
        self._impl.interface.on_change()


class Switch(TextViewWidget, ContainedWidget):
    focusable = False

    def create(self):
        self.native = A_Switch(self._native_activity)
        self.native.setOnCheckedChangeListener(OnCheckedChangeListener(self))
        self.cache_textview_defaults()

    def get_text(self):
        return str(self.native.getText())

    def set_text(self, text):
        # When changing the text, Android needs a `setSingleLine(False)` call in order
        # to be willing to recompute the width of the text. Without the call, it will
        # constrain the new text to have the same line width as the old text, resulting
        # in unnecessary creation of new lines. In other words, `setSingleLine(False)`
        # is required to get the text to truly **use** one single line!
        self.native.setSingleLine(False)
        self.native.setText(str(text))

    def get_value(self):
        return self.native.isChecked()

    def set_value(self, value):
        self.native.setChecked(bool(value))

    def rehint(self):
        self.native.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.getMeasuredWidth()), ROUND_UP
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.getMeasuredHeight(), ROUND_UP
        )
