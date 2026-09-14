from travertino.colors import Color
from travertino.constants import CENTER, INDIANRED, JUSTIFY, LEFT, RED, RIGHT
from travertino.size import at_least
from win32more.Microsoft.UI.Xaml import TextAlignment, Visibility
from win32more.Microsoft.UI.Xaml.Controls import TextBox, ToolTip, ToolTipService
from win32more.Windows.System import VirtualKey

from ..colors import native_brush
from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native_cls = TextBox

        self._tool_tip = ToolTip()

        # Initial minimum sizes are 0 because the staged properties are delayed, and
        # this allows to the widget to be sized up.
        self._min_width = 0
        self._min_height = 0

        def initial_text():
            return "\u200b"

        self._staged_properties.Text = initial_text
        self.native.Text = ""

        self.native.event_handler.TextChanging += self.native_event_text_changing
        self.native.event_handler.KeyDown += self.native_event_key_down
        self.native.event_handler.GotFocus += self.native_event_got_focus
        self.native.event_handler.LostFocus += self.native_event_lost_focus

    ####################################################################################
    # Native events.
    ####################################################################################

    def native_event_text_changing(self, sender, args):
        # NOTE: This event is fired synchronously after the text is changed, but before
        # it is rendered. The alternative event, TextChanged fires asynchronously, after
        # the text is changed.
        self.interface._value_changed()

    def native_event_key_down(self, sender, args):
        if args.Key == VirtualKey.Enter:
            self.interface.on_confirm()
            args.Handled = True

    def native_event_got_focus(self, sender, event):
        self.interface.on_gain_focus()

    def native_event_lost_focus(self, sender, event):
        self.interface.on_lose_focus()

    ####################################################################################
    # Methods called by the Toga core interface.
    ####################################################################################

    def get_readonly(self):
        return self.native.IsReadOnly

    def set_readonly(self, value):
        self.native.IsReadOnly = value

    def get_placeholder(self):
        return self.native.PlaceholderText

    def set_placeholder(self, value: str):
        self.native.PlaceholderText = value

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = value

    def is_valid(self):
        return ToolTipService.GetToolTip(self.native) is None

    def clear_error(self):
        self.native.Resources.Remove("TextControlBorderBrushFocused")
        self.native.Resources.Remove("TextControlBorderBrushPointerOver")
        self._native_properties.BorderBrush = None

        # This code block forces a reloading of the style properties which were
        # overridden by the local resources dictionary.
        if not self.is_valid():
            has_focus = self.has_focus

            is_hidden = self.native.Visibility == Visibility.Collapsed
            self.set_hidden(hidden=True)
            self.set_hidden(hidden=is_hidden)

            if has_focus:
                self.focus()

        ToolTipService.SetToolTip(self.native, None)

    def set_error(self, error_message):
        self.native.Resources["TextControlBorderBrushFocused"] = native_brush(
            Color.parse(INDIANRED)
        )
        self.native.Resources["TextControlBorderBrushPointerOver"] = native_brush(
            Color.parse(RED)
        )
        self._native_properties.BorderBrush = native_brush(Color.parse(RED))

        self._tool_tip.Content = error_message
        ToolTipService.SetToolTip(self.native, self._tool_tip)

    ####################################################################################
    # Overrides of methods called by the Toga style applicator.
    ####################################################################################

    def set_text_align(self, alignment):
        property_dict = {
            CENTER: "Center",
            JUSTIFY: "Justify",
            LEFT: "Left",
            RIGHT: "Right",
        }
        property = property_dict[alignment]
        native_alignment = getattr(TextAlignment, property)

        self._native_properties.TextAlignment = native_alignment

    ####################################################################################
    # Overrides of other methods called by the Toga core interface.
    ####################################################################################

    def rehint(self):
        self.interface.intrinsic.width = at_least(self._min_width)
        self.interface.intrinsic.height = self._min_height
