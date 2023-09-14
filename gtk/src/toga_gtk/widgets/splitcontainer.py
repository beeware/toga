from travertino.size import at_least

from ..container import TogaContainer
from ..libs import Gtk
from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self.native = Gtk.Paned()
        self.native.set_wide_handle(True)

        self.sub_containers = [TogaContainer(), TogaContainer()]
        self.native.pack1(self.sub_containers[0], True, False)
        self.native.pack2(self.sub_containers[1], True, False)

        self._split_proportion = 0.5

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # If we've got a pending split to apply, set the split position.
        # However, only do this if the layout is more than the min size;
        # there are initial 0-sized layouts for which the split is meaningless.
        if (
            self._split_proportion
            and width >= self.interface._MIN_WIDTH
            and height > self.interface._MIN_HEIGHT
        ):
            if self.interface.direction == self.interface.VERTICAL:
                position = int(self._split_proportion * width)
            else:
                position = int(self._split_proportion * height)

            self.native.set_position(position)
            self._split_proportion = None

    def set_content(self, content, flex):
        # Clear any existing content
        for container in self.sub_containers:
            container.content = None

        # Add all children to the content widget.
        for position, widget in enumerate(content):
            self.sub_containers[position].content = widget

        # We now know the initial positions of the split. However, we can't *set* the
        # because GTK requires a pixel position, and the widget isn't visible yet. So -
        # store the split; and when we do our first layout, apply that proportion.
        self._split_proportion = flex[0] / sum(flex)

    def get_direction(self):
        if self.native.get_orientation() == Gtk.Orientation.HORIZONTAL:
            return self.interface.VERTICAL
        else:
            return self.interface.HORIZONTAL

    def set_direction(self, value):
        if value == self.interface.VERTICAL:
            self.native.set_orientation(Gtk.Orientation.HORIZONTAL)
        else:
            self.native.set_orientation(Gtk.Orientation.VERTICAL)

    def rehint(self):
        # This is a SWAG (scientific wild-ass guess). There doesn't appear to be
        # an actual API to get the true size of the splitter. 10px seems enough.
        SPLITTER_WIDTH = 10
        if self.interface.direction == self.interface.HORIZONTAL:
            # When the splitter is horizontal, the splitcontainer must be
            # at least as wide as it's widest sub-container, and at least
            # as tall as the minimum height of all subcontainers, plus the
            # height of the splitter itself. Enforce a minimum size in both
            # axies
            min_width = self.interface._MIN_WIDTH
            min_height = 0
            for sub_container in self.sub_containers:
                # Make sure the subcontainer's size is up to date
                sub_container.recompute()

                min_width = max(min_width, sub_container.min_width)
                min_height += sub_container.min_height

            min_height = max(min_height, self.interface._MIN_HEIGHT) + SPLITTER_WIDTH
        else:
            # When the splitter is vertical, the splitcontainer must be
            # at least as tall as it's tallest sub-container, and at least
            # as wide as the minimum width of all subcontainers, plus the
            # width of the splitter itself.
            min_width = 0
            min_height = self.interface._MIN_HEIGHT
            for sub_container in self.sub_containers:
                # Make sure the subcontainer's size is up to date
                sub_container.recompute()

                min_width += sub_container.min_width
                min_height = max(min_height, sub_container.min_height)

            min_width = max(min_width, self.interface._MIN_WIDTH) + SPLITTER_WIDTH

        self.interface.intrinsic.width = at_least(min_width)
        self.interface.intrinsic.height = at_least(min_height)
