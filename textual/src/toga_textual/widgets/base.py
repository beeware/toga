from travertino.size import at_least

from toga.style.pack import ROW
from toga.types import Size


# We assume a terminal is 800x600 pixels, mapping to 80x25 characters.
# This results in an uneven scale in the horizontal and vertical directions.
class Scalable:
    HORIZONTAL_SCALE = 800 // 80
    VERTICAL_SCALE = 600 // 25

    def scale_in_horizontal(self, value):
        return value // self.HORIZONTAL_SCALE

    def scale_out_horizontal(self, value):
        try:
            return at_least(value.value * self.HORIZONTAL_SCALE)
        except AttributeError:
            return value * self.HORIZONTAL_SCALE

    def scale_in_vertical(self, value):
        return value // self.VERTICAL_SCALE

    def scale_out_vertical(self, value):
        try:
            return at_least(value.value * self.VERTICAL_SCALE)
        except AttributeError:
            return value * self.VERTICAL_SCALE


class Widget(Scalable):
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    def install(self, parent):
        """Add widget and its children to the native DOM for the app.

        Textual does not allow widgets to be added to the DOM until their parent is
        added. Therefore, when children are added to an unmounted widget, their
        mounting is deferred until their parent is mounted.
        """
        parent.native.mount(self.native)

        for child in self.interface.children:
            child._impl.install(parent=self)

    def get_size(self) -> Size:
        return Size(0, 0)

    def create(self):
        pass

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    def get_enabled(self):
        return not self.native.disabled

    def set_enabled(self, value):
        self.native.disabled = not value

    def focus(self):
        pass

    def get_tab_index(self):
        return None

    def set_tab_index(self, tab_index):
        pass

    ######################################################################
    # APPLICATOR
    ######################################################################

    def set_bounds(self, x, y, width, height):
        # Convert the width and height back into terminal coordinates
        self.native.styles.width = self.scale_in_horizontal(width)
        self.native.styles.height = self.scale_in_vertical(height)

        # Positions are more complicated. The (x,y) provided as an argument is
        # in absolute coordinates. The `content_left` ad `content_right` values
        # of the layout are relative coordinate. Textual doesn't allow specifying
        # either absolute *or* relative - we can only specify margin values within
        # a row/column box. This means we need to reverse engineer the margins from
        # the computed layout.
        parent = self.interface.parent
        if parent is None:
            # Root object in a layout; Margins are the literal content offsets
            margin_top = self.interface.layout.content_top
            margin_right = self.interface.layout.content_right
            margin_bottom = self.interface.layout.content_bottom
            margin_left = self.interface.layout.content_left
        else:
            # Look for this widget in the children of the parent
            index = parent.children.index(self.interface)
            if index == 0:
                # First child in the container; margins are the literal content offsets
                margin_top = self.interface.layout.content_top
                margin_right = self.interface.layout.content_right
                margin_bottom = self.interface.layout.content_bottom
                margin_left = self.interface.layout.content_left
            else:
                # 2nd+ child in the container. Right and Bottom content offsets are as
                # computed by layout. If the parent is a row box, the top offset is as
                # computed, but the left offset must be computed relative to the right
                # margin of the predecessor. If the parent is a column box, the left
                # offset is as computed, but the top offset must be computed relative to
                # the bottom margin of the predecessor.
                predecessor = parent.children[index - 1]

                margin_top = self.interface.layout.content_top
                margin_right = self.interface.layout.content_right
                margin_bottom = self.interface.layout.content_bottom
                margin_left = self.interface.layout.content_left

                # The layout doesn't have a concept of flow direction; this is a
                # property of the style language. However, we don't have any other way
                # to establish whether this is a row or a column box.
                if parent.style.direction == ROW:
                    margin_left -= (
                        predecessor.layout.content_left
                        + predecessor.layout.content_width
                        + predecessor.layout.content_right
                    )
                else:
                    margin_top -= (
                        predecessor.layout.content_top
                        + predecessor.layout.content_height
                        + predecessor.layout.content_bottom
                    )

        # Convert back into terminal coordinates, and apply margins to the widget.
        self.native.styles.margin = (
            self.scale_in_vertical(margin_top),
            self.scale_in_horizontal(margin_right),
            self.scale_in_vertical(margin_bottom),
            self.scale_in_horizontal(margin_left),
        )

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        pass

    def set_font(self, font):
        pass

    def set_color(self, color):
        pass

    def set_background_color(self, color):
        pass

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        # A child can only be added to a widget that is already mounted on the app.
        # So, mounting the child is deferred if the parent is not mounted yet.
        if self.native.is_attached:
            self.native.mount(child.native)

    def insert_child(self, index, child):
        pass

    def remove_child(self, child):
        self.native.remove_children([child.native])

    def refresh(self):
        intrinsic = self.interface.intrinsic
        intrinsic.width = intrinsic.height = None
        self.rehint()
        assert intrinsic.width is not None
        assert intrinsic.height is not None

        intrinsic.width = self.scale_out_horizontal(intrinsic.width)
        intrinsic.height = self.scale_out_vertical(intrinsic.height)
