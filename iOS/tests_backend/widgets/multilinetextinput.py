import asyncio

from toga_iOS.libs import UITextView

from .textinput import TextInputProbe


class MultilineTextInputProbe(TextInputProbe):
    native_class = UITextView

    @property
    def value(self):
        return str(
            self.native.placeholder_label.text
            if self.placeholder_visible
            else self.native.text
        )

    @property
    def placeholder_visible(self):
        return not self.native.placeholder_label.isHidden()

    @property
    def placeholder_hides_on_focus(self):
        return True

    @property
    def readonly(self):
        return not self.native.isEditable()

    @property
    def document_height(self):
        return max(self.native.contentSize.height, self.native.frame.size.height)

    @property
    def document_width(self):
        return max(self.native.contentSize.width, self.native.frame.size.width)

    @property
    def vertical_scroll_position(self):
        return self.native.contentOffset.y

    async def wait_for_scroll_completion(self):
        position = self.vertical_scroll_position
        current = None
        # Iterate until 2 successive reads of the scroll position,
        # 0.05s apart, return the same value
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = self.vertical_scroll_position
