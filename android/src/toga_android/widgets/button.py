from decimal import ROUND_UP

from android.view import View
from android.widget import Button as A_Button
from java import dynamic_proxy
from travertino.size import at_least

from toga.colors import TRANSPARENT

from .label import TextViewWidget

try:
    from com.google.android.material.button import MaterialButton
except ImportError:  # pragma: no cover
    # Older projects that don't include the Material library; fall back to a plain
    # android.widget.Button. Can't be validated in CI, so it's marked no-cover.
    MaterialButton = None


class TogaOnClickListener(dynamic_proxy(View.OnClickListener)):
    def __init__(self, button_impl):
        super().__init__()
        self.button_impl = button_impl

    def onClick(self, _view):
        self.button_impl.interface.on_press()


class Button(TextViewWidget):
    focusable = False

    # Tri-state cache of whether a MaterialButton can be created under the app's
    # theme. MaterialButton requires a Material Components / Material 3 theme and
    # raises if the theme doesn't qualify, so we probe once: None = not yet probed,
    # True/False = the result. Cached on the class because the theme is app-wide.
    _material_capable = None

    def create(self):
        self.native = self._create_native_button()
        self.native.setOnClickListener(TogaOnClickListener(button_impl=self))
        self.cache_textview_defaults()

        self._icon = None

    def _create_native_button(self):
        # Prefer a Material "filled" button (rounded, ripple, accent-tinted from the
        # theme's colorPrimary) when the Material library is present AND the app theme
        # supports it. A plain Button is used otherwise, so AppCompat-themed apps are
        # unaffected. MaterialButton subclasses android.widget.Button, so the rest of
        # this backend (and the probe's isinstance check) still applies.
        if MaterialButton is not None and Button._material_capable is not False:
            try:
                button = MaterialButton(self._native_activity)
                Button._material_capable = True
                return button
            except Exception:  # pragma: no cover - theme isn't Material-compatible
                Button._material_capable = False
        return A_Button(self._native_activity)

    def get_text(self):
        return str(self.native.getText())

    def set_text(self, text):
        self.native.setText(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            # Scale icon to to a 48x48 CSS pixel bitmap drawable.
            drawable = icon._impl.as_drawable(self, 48)
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
            # "measured" size. Hardcode a button size of 48x48 pixels with 10px of
            # padding (in CSS pixels).
            self.interface.intrinsic.width = at_least(68)
            self.interface.intrinsic.height = 68
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
