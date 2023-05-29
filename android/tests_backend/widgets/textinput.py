from java import jclass

from android.os import SystemClock
from android.text import InputType
from android.view import KeyEvent
from android.view.inputmethod import EditorInfo

from .label import LabelProbe


class TextInputProbe(LabelProbe):
    native_class = jclass("android.widget.EditText")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_connection = self.native.onCreateInputConnection(EditorInfo())

    @property
    def value(self):
        return self.native.getHint() if self.placeholder_visible else self.text

    @property
    def value_hidden(self):
        return bool(self.native.getInputType() & InputType.TYPE_TEXT_VARIATION_PASSWORD)

    @property
    def placeholder_visible(self):
        return not self.text

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def readonly(self):
        focusable = self.native.isFocusable()
        focusable_in_touch_mode = self.native.isFocusableInTouchMode()
        if focusable != focusable_in_touch_mode:
            raise ValueError(f"invalid state: {focusable=}, {focusable_in_touch_mode=}")
        return not focusable

    async def type_character(self, char):
        try:
            key_code = {
                "<esc>": KeyEvent.KEYCODE_ESCAPE,
                " ": KeyEvent.KEYCODE_SPACE,
                "\n": KeyEvent.KEYCODE_ENTER,
            }[char]
        except KeyError:
            assert len(char) == 1, char
            key_code = getattr(KeyEvent, f"KEYCODE_{char.upper()}")

        timestamp = SystemClock.uptimeMillis()
        for action in [KeyEvent.ACTION_DOWN, KeyEvent.ACTION_UP]:
            self._input_connection.sendKeyEvent(
                KeyEvent(
                    timestamp,  # downTime
                    timestamp,  # eventTime
                    action,
                    key_code,
                    0,  # repeat
                    KeyEvent.META_SHIFT_ON if char.isupper() else 0,
                )
            )
