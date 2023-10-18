import pytest
from android.os import SystemClock
from android.text import InputType
from android.view import KeyEvent
from android.view.inputmethod import EditorInfo
from java import jclass

from .label import LabelProbe


class TextInputProbe(LabelProbe):
    native_class = jclass("android.widget.EditText")
    default_font_size = 18

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

        # Check if TYPE_TEXT_FLAG_NO_SUGGESTIONS is set in the input type
        input_type = self.native.getInputType()
        if input_type & InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS:
            # TYPE_TEXT_FLAG_NO_SUGGESTIONS is set
            if focusable:
                raise ValueError(
                    "TYPE_TEXT_FLAG_NO_SUGGESTIONS is not set on the input."
                )
        else:
            # TYPE_TEXT_FLAG_NO_SUGGESTIONS is not set
            if not focusable:
                raise ValueError(
                    "TYPE_TEXT_FLAG_NO_SUGGESTIONS has been set when the input is readonly."
                )

        return not focusable

    async def type_character(self, char):
        # In CI, sendKeyEvent logs the warning "Cancelling event (no window focus)", and
        # doesn't trigger on_change. So we only use it for the special keys needed by
        # the on_confirm test.
        try:
            key_code = {
                "<esc>": KeyEvent.KEYCODE_ESCAPE,
                "\n": KeyEvent.KEYCODE_ENTER,
            }[char]
        except KeyError:
            self.native.append(char)
        else:
            timestamp = SystemClock.uptimeMillis()
            for action in [KeyEvent.ACTION_DOWN, KeyEvent.ACTION_UP]:
                self._input_connection.sendKeyEvent(
                    KeyEvent(
                        timestamp,  # downTime
                        timestamp,  # eventTime
                        action,
                        key_code,
                        0,  # repeat
                        0,  # metaState
                    )
                )

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
