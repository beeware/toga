from textual.widgets import TextArea as TextualTextArea
from travertino.size import at_least

from .base import Widget


class TogaTextArea(TextualTextArea):
    def __init__(self, impl):
        super().__init__(
            "",
            soft_wrap=True,
            tab_behavior="focus",
            read_only=False,
            show_line_numbers=False,
        )
        self.interface = impl.interface
        self.impl = impl

    def on_focus(self, event) -> None:
        self.impl.on_focus()

    def on_blur(self, event) -> None:
        self.impl.on_blur()

    def on_text_area_changed(self, event: TextualTextArea.Changed) -> None:
        self.impl.on_text_changed()


class MultilineTextInput(Widget):
    def create(self):
        self._value = ""
        self._placeholder = ""
        self._placeholder_visible = False
        self._programmatic_changes = 0
        self.native = TogaTextArea(self)

    @property
    def placeholder_visible(self):
        return self._placeholder_visible

    def _load_text(self, value):
        self._programmatic_changes += 1
        self.native.load_text(value)

    def _display_placeholder(self):
        return (
            self._value == "" and self._placeholder != "" and not self.native.has_focus
        )

    def _sync_display(self):
        placeholder_visible = self._display_placeholder()
        display_text = self._placeholder if placeholder_visible else self._value
        self._placeholder_visible = placeholder_visible

        if self.native.text != display_text:
            self._load_text(display_text)

    def on_focus(self):
        if self._placeholder_visible:
            self._placeholder_visible = False
            self._load_text("")

    def on_blur(self):
        if self._value == "" and self._placeholder != "":
            self._placeholder_visible = True
            self._load_text(self._placeholder)

    def on_text_changed(self):
        if self._programmatic_changes:
            self._programmatic_changes -= 1
            return

        if self._placeholder_visible:
            return

        self._value = self.native.text
        self.interface.on_change()

    def get_value(self):
        return self._value

    def set_value(self, value):
        old_value = self._value
        self._value = value
        self._sync_display()

        if value != old_value:
            self.interface.on_change()

    def get_readonly(self):
        return self.native.read_only

    def set_readonly(self, value):
        self.native.read_only = value
        self.native.show_cursor = not value

    def get_placeholder(self):
        return self._placeholder

    def set_placeholder(self, value):
        self._placeholder = value
        self._sync_display()

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            self.scale_in_vertical(self.interface._MIN_HEIGHT)
        )

    def scroll_to_bottom(self):
        self.native.scroll_end(
            animate=False,
            force=True,
            immediate=True,
            x_axis=False,
        )

    def scroll_to_top(self):
        self.native.scroll_home(
            animate=False,
            force=True,
            immediate=True,
            x_axis=False,
        )
