import System.Windows.Forms as WinForms
from System.Drawing import SystemColors
from travertino.size import at_least

from toga_winforms.colors import native_color
from toga_winforms.libs.fonts import HorizontalTextAlignment

from ..libs.wrapper import WeakrefCallable
from .textinput import TextInput


class MultilineTextInput(TextInput):
    def create(self):
        # TextBox doesn't support automatic scroll bar visibility, so we use RichTextBox
        # (https://stackoverflow.com/a/612234).
        self.native = WinForms.RichTextBox()
        self.native.Multiline = True
        self.native.TextChanged += WeakrefCallable(self.winforms_text_changed)

        # When moving focus with the tab key, the Enter/Leave event handlers see the
        # wrong value of ContainsFocus, so we use GotFocus/LostFocus instead.
        self.native.GotFocus += WeakrefCallable(self.winforms_got_focus)
        self.native.LostFocus += WeakrefCallable(self.winforms_lost_focus)

        # Dummy values used during initialization
        self._placeholder = ""
        self._placeholder_visible = True
        self.set_color(None)

    def winforms_got_focus(self, sender, event):
        # If the placeholder is visible when we gain focus, the widget is empty;
        # so make the native text empty and hide the placeholder.
        if self._placeholder_visible:
            self.native.Text = ""
            self._set_placeholder_visible(False)

    def winforms_lost_focus(self, sender, event):
        # When we lose focus, if the widget is empty, we need to show the
        # placeholder again.
        if self.native.Text == "":
            self._set_placeholder_visible(True)

    def set_placeholder(self, value):
        self._placeholder = value
        if self._placeholder_visible:
            self.native.Text = value

    def get_value(self):
        # If the placeholder is visible, we know the widget has no value
        if self._placeholder_visible:
            return ""
        return self.native.Text

    def set_value(self, value):
        # If the value is empty, the placeholder is only visible if the widget
        # does *not* currently have focus.
        if value == "" and not self.native.ContainsFocus:
            self.native.Text = value
            self._set_placeholder_visible(True)
        else:
            self._set_placeholder_visible(False)
            self.native.Text = value

    # This method is necessary to override the TextInput base class.
    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def winforms_text_changed(self, sender, event):
        # Showing and hiding the placeholder should not cause an interface event.
        if not self._placeholder_visible:
            self.interface.on_change()

    def _set_placeholder_visible(self, visible):
        # Changing ForeColor causes a native TextChanged event, so the order of these
        # lines is important.
        if visible:
            self._placeholder_visible = True
            self.native.Text = self._placeholder
            self.native.ForeColor = SystemColors.GrayText
        elif self._placeholder_visible:
            self.native.ForeColor = self._color
            self._placeholder_visible = False

    def set_color(self, color):
        self._color = (
            SystemColors.WindowText if (color is None) else native_color(color)
        )
        if not self._placeholder_visible:
            self.native.ForeColor = self._color

    def set_alignment(self, value):
        original_selection = (self.native.SelectionStart, self.native.SelectionLength)
        self.native.SelectAll()
        self.native.SelectionAlignment = HorizontalTextAlignment(value)
        self.native.SelectionStart, self.native.SelectionLength = original_selection

    def scroll_to_bottom(self):
        self.native.SelectionStart = len(self.native.Text)
        self.native.ScrollToCaret()

    def scroll_to_top(self):
        self.native.SelectionStart = 0
        self.native.ScrollToCaret()
