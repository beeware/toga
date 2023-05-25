import System.Windows.Forms
from System.Drawing import SystemColors

from toga.style.pack import TOP

from .base import SimpleProbe
from .properties import toga_xalignment


class MultilineTextInputProbe(SimpleProbe):
    native_class = System.Windows.Forms.RichTextBox
    background_supports_alpha = False

    @property
    def value(self):
        return self.native.Text

    @property
    def placeholder_visible(self):
        return self.native.ForeColor == SystemColors.GrayText

    @property
    def placeholder_hides_on_focus(self):
        return True

    @property
    def readonly(self):
        return self.native.ReadOnly

    def _char_pos(self, index):
        return self.native.GetPositionFromCharIndex(index)

    @property
    def document_height(self):
        text_len = len(self.native.Text)
        height = self._char_pos(text_len - 1).Y - self._char_pos(0).Y

        line_count = self.native.GetLineFromCharIndex(text_len - 1) + 1
        if line_count > 1:
            # Scale up to include the final line.
            assert height > 0
            height *= line_count / (line_count - 1)

        return height / self.scale_factor

    @property
    def document_width(self):
        return self.width

    @property
    def vertical_scroll_position(self):
        return -(self._char_pos(0).Y) / self.scale_factor

    async def wait_for_scroll_completion(self):
        pass

    async def type_character(self, char):
        self.native.AppendText(char)

    # According to the documentation: "SelectionAlignment returns
    # SelectionAlignment.Left when the text selection contains multiple paragraphs with
    # mixed alignment."
    @property
    def alignment(self):
        self.native.SelectAll()
        return toga_xalignment(self.native.SelectionAlignment)

    @property
    def vertical_alignment(self):
        return TOP
