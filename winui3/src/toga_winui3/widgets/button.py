from travertino.size import at_least
from win32more.Microsoft.UI.Xaml.Controls import Button as NativeButton

from toga.constants import TRANSPARENT

from .base import Widget


class Button(Widget):
    def create(self):
        # Setting native_cls defines self.native and means that events are managed by
        # the nativeevents module.
        self.native_cls = NativeButton

        self._icon = None
        self._text = ""

        # Initial minimum sizes are 0 because the staged properties are delayed, and
        # this allows to the widget to be sized up.
        self._min_width = 0
        self._min_height = 0

        self.native.event_handler.Click += self.native_event_click

    def native_event_click(self, sender, args):
        self.interface.on_press()

    ####################################################################################
    # Button content
    ####################################################################################

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

        if self._icon is not None:
            return

        self._staged_properties.Content = self.text

    def text(self):
        # "\u200b" (ZERO WIDTH SPACE) instead of "" ensures correct button height.
        return "\u200b" if self._text == "" else self._text

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon

        if icon is None:
            return

        self._staged_properties.Content = self.icon

    def icon(self):
        return self._icon._impl.image_icon(32)

    ####################################################################################
    # Overrides of methods called by the Toga style applicator.
    ####################################################################################

    def set_background_color(self, color):
        color = None if color is TRANSPARENT else color
        super().set_background_color(color)

    def set_text_align(self, alignment):
        # FIXME: WinUI 3 has the ability to set the content alignment of a button, but
        # the Toga style will default to either left-aligned or right-aligned which is
        # different from the default WinUI 3 value of center-aligned.
        pass

    ####################################################################################
    # Overrides of other methods called by the Toga core interface.
    ####################################################################################

    def rehint(self):
        self.interface.intrinsic.width = at_least(self._min_width)
        self.interface.intrinsic.height = self._min_height
