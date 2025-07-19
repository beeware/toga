from decimal import ROUND_UP

from android.view import View
from android.widget import Button as A_Button
from java import dynamic_proxy
from travertino.size import at_least

from toga.colors import TRANSPARENT

from .label import TextViewWidget

DEFAULT_ICON_SIZE = 48


class TogaOnClickListener(dynamic_proxy(View.OnClickListener)):
    def __init__(self, button_impl):
        super().__init__()
        self.button_impl = button_impl

    def onClick(self, _view):
        self.button_impl.interface.on_press()


class Button(TextViewWidget):
    focusable = False

    def create(self):
        self.native = A_Button(self._native_activity)
        self.native.setOnClickListener(TogaOnClickListener(button_impl=self))
        self.cache_textview_defaults()

        self._icon = None

    def get_text(self):
        return str(self.native.getText())

    def set_text(self, text):
        self.native.setText(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            # Scale icon to a CSS pixel bitmap drawable (default to 48x48 if the size
            # hasn't been provided).
            drawable = icon._impl.as_drawable(self, DEFAULT_ICON_SIZE)
        else:
            drawable = None

        self.native.setCompoundDrawablesRelative(drawable, None, None, None)

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def set_background_color(self, color):
        self.set_background_filter(None if color is TRANSPARENT else color)

    def rehint(self):
        if self._icon:
            # Icons aren't considered "inside" the button, so they aren't part of the
            # "measured" size. Hardcode a button size of the icon size (or the 48x48
            # pixels default) with 10px of padding on each side (in CSS pixels).
            size = 20 + (
                DEFAULT_ICON_SIZE if self._icon.size is None else self._icon.size
            )
            self.interface.intrinsic.width = at_least(size)
            self.interface.intrinsic.height = size
        else:
            self.native.measure(
                View.MeasureSpec.UNSPECIFIED,
                View.MeasureSpec.UNSPECIFIED,
            )
            self.interface.intrinsic.width = self.scale_out(
                at_least(self.native.getMeasuredWidth()), ROUND_UP
            )
            self.interface.intrinsic.height = self.scale_out(
                self.native.getMeasuredHeight(), ROUND_UP
            )
