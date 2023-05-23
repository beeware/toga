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
