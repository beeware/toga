from decimal import ROUND_UP

from android.text import InputType, TextWatcher
from android.view import Gravity, View
from android.widget import EditText
from java import dynamic_proxy

from toga_android.keys import toga_key

from .label import TextViewWidget


class TogaTextWatcher(dynamic_proxy(TextWatcher)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def beforeTextChanged(self, _charSequence, _start, _count, _after):
        pass

    def afterTextChanged(self, _editable):
        self.impl._on_change()

    def onTextChanged(self, _charSequence, _start, _before, _count):
        pass


class TogaKeyListener(dynamic_proxy(View.OnKeyListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onKey(self, _view, _key, _event):
        event_info = toga_key(_event)
        if event_info is None:
            pass  # pragma: nocover
        else:
            key_pressed = event_info["key"].value
            if (key_pressed == "<enter>" or key_pressed == "numpad:enter") and (
                int(_event.getAction()) == 1
            ):
                self.impl._on_confirm()
        return False


class TogaFocusListener(dynamic_proxy(View.OnFocusChangeListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onFocusChange(self, view, has_focus):
        if has_focus:
            self.impl._on_gain_focus()
        else:
            self.impl._on_lose_focus()


class TextInput(TextViewWidget):
    def create(self, input_type=InputType.TYPE_CLASS_TEXT):
        self.native = EditText(self._native_activity)
        self.native.setInputType(input_type)
        self.cache_textview_defaults()

        self.native.addTextChangedListener(TogaTextWatcher(self))
        self.native.setOnKeyListener(TogaKeyListener(self))
        self.native.setOnFocusChangeListener(TogaFocusListener(self))

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
            # Add TYPE_TEXT_FLAG_NO_SUGGESTIONS to the input type to disable suggestions
            input_type = (
                self.native.getInputType() | InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS
            )
            self.native.setInputType(input_type)
        else:
            # Implicitly calls setFocusable(True)
            self.native.setFocusableInTouchMode(True)
            # Remove TYPE_TEXT_FLAG_NO_SUGGESTIONS to enable suggestions
            input_type = (
                self.native.getInputType() & ~InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS
            )
            self.native.setInputType(input_type)

    def get_placeholder(self):
        return str(self.native.getHint())

    def set_placeholder(self, value):
        self.native.setHint(value)

    def set_alignment(self, value):
        self.set_textview_alignment(value, Gravity.CENTER_VERTICAL)

    def set_error(self, error_message):
        self.native.setError(error_message)

    def clear_error(self):
        self.native.setError(None)

    def is_valid(self):
        return self.native.getError() is None

    def _on_change(self):
        self.interface._value_changed()

    def _on_confirm(self):
        self.interface.on_confirm()

    def _on_gain_focus(self):
        self.interface.on_gain_focus()

    def _on_lose_focus(self):
        self.interface.on_lose_focus()

    def rehint(self):
        self.native.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        self.interface.intrinsic.height = self.scale_out(
            self.native.getMeasuredHeight(), ROUND_UP
        )
