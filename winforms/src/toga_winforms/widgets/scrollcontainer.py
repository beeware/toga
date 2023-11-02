from decimal import ROUND_DOWN

from System.Drawing import Point
from System.Windows.Forms import Panel, SystemInformation
from travertino.node import Node

from toga_winforms.container import Container

from ..libs.wrapper import WeakrefCallable
from .base import Widget

# On Windows, scroll bars usually appear only when the content is larger than the
# container. However, this complicates layout. For example, if the content fits in
# the container horizontally but is taller vertically, we then need to do a second
# layout pass with a slightly narrower horizontal size to account for the vertical
# scroll bar (https://stackoverflow.com/questions/28418026).
#
# A previous attempt to avoid this, by making the scroll bars always visible, was not
# successful (see commit "Initial Winforms implementation" on 2023-07-10). Although the
# ScrollableControl API does provide Visible and Enabled properties for each scroll bar,
# they behave in confusing and undocumented ways, e.g.:
#
#  * https://stackoverflow.com/questions/8690643
#  * https://stackoverflow.com/questions/5489273
#
# So the current implementation just uses the default AutoScroll behavior, and does a
# second layout pass where necessary.


class ScrollContainer(Widget, Container):
    def create(self):
        self.native = Panel()
        self.native.AutoScroll = True
        Container.__init__(self, self.native)

        # The Scroll event only fires on direct interaction with the scroll bar. It
        # doesn't fire when using the mouse wheel, and it doesn't fire when setting
        # AutoScrollPosition either, despite the documentation saying otherwise.
        self.native.Scroll += WeakrefCallable(self.winforms_scroll)
        self.native.MouseWheel += WeakrefCallable(self.winforms_scroll)

    def winforms_scroll(self, sender, event):
        self.interface.on_scroll()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.resize_content(
            self.scale_in(width, ROUND_DOWN),
            self.scale_in(height, ROUND_DOWN),
        )

    def refreshed(self):
        full_width, full_height = (self.native_width, self.native_height)
        inset_width = full_width - SystemInformation.VerticalScrollBarWidth
        inset_height = full_height - SystemInformation.HorizontalScrollBarHeight
        layout = self.interface.content.layout

        # Temporarily reduce container size to account for scroll bars (see explanation
        # at the top of this file).
        def apply_insets():
            need_scrollbar = False
            if self.vertical and (layout.height > self.height):
                need_scrollbar = True
                self.native_width = inset_width
            if self.horizontal and (layout.width > self.width):
                need_scrollbar = True
                self.native_height = inset_height
            return need_scrollbar

        if apply_insets():
            # Bypass Widget.refresh to avoid a recursive call to `refreshed`.
            Node.refresh(self.interface.content, self)

            # In borderline cases, adding one scroll bar may cause the other one to be
            # needed as well.
            apply_insets()

        # Crop any non-scrollable dimensions to the available size.
        self.apply_layout(
            layout.width if self.horizontal else 0,
            layout.height if self.vertical else 0,
        )

        # Restore the original container size so it'll be used in the next call to
        # `refresh` or `resize_content`.
        self.native_width, self.native_height = full_width, full_height

    def get_horizontal(self):
        return self.horizontal

    def set_horizontal(self, value):
        self.horizontal = value
        if not value:
            self.interface.on_scroll()
        if self.interface.content:
            self.interface.content.refresh()

    def get_vertical(self):
        return self.vertical

    def set_vertical(self, value):
        self.vertical = value
        if not value:
            self.interface.on_scroll()
        if self.interface.content:
            self.interface.content.refresh()

    def get_vertical_position(self):
        return self.scale_out(abs(self.native.AutoScrollPosition.Y))

    def get_horizontal_position(self):
        return self.scale_out(abs(self.native.AutoScrollPosition.X))

    def get_max_vertical_position(self):
        return self.scale_out(
            max(0, self.native_content.Height - self.native.ClientSize.Height)
        )

    def get_max_horizontal_position(self):
        return self.scale_out(
            max(0, self.native_content.Width - self.native.ClientSize.Width)
        )

    def set_position(self, horizontal_position, vertical_position):
        self.native.AutoScrollPosition = Point(
            self.scale_in(horizontal_position),
            self.scale_in(vertical_position),
        )
        self.interface.on_scroll()
