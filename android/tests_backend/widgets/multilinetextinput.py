from java import jclass

from .label import LabelProbe


class MultilineTextInputProbe(LabelProbe):
    native_class = jclass("android.widget.EditText")

    @property
    def value(self):
        return self.text

    @property
    def placeholder(self):
        return str(self.native.getHint())

    def placeholder_visible(self):
        return not self.value

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def enabled(self):
        return not self.readonly

    @property
    def readonly(self):
        focusable = self.native.isFocusable()
        focusable_in_touch_mode = self.native.isFocusableInTouchMode()
        if focusable != focusable_in_touch_mode:
            raise ValueError(f"invalid state: {focusable=}, {focusable_in_touch_mode=}")
        return not focusable

    @property
    def visible_height(self):
        return self.height

    @property
    def visible_width(self):
        return self.width

    @property
    def document_height(self):
        return self.native.getLayout().getHeight()

    @property
    def document_width(self):
        return self.native.getLayout().getWidth()

    @property
    def vertical_scroll_position(self):
        return self.native.getScrollY()

    async def wait_for_scroll_completion(self):
        pass
