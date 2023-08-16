from travertino.size import at_least


# We assume a terminal is 800x600 pixels, mapping to 80x25 characters.
# This results in an uneven scale in the horizontal and vertical directions
class Scalable:
    HORIZONTAL_SCALE = 10
    VERTICAL_SCALE = 25

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

    def get_size(self):
        return (0, 0)

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

    @property
    def width_adjustment(self):
        return 0

    @property
    def height_adjustment(self):
        return 0

    def set_bounds(self, x, y, width, height):
        # Convert the width and height back into terminal coordinates,
        # subtracting the extra spacing associated with the widget itself.
        self.native.styles.width = (
            self.scale_in_horizontal(width) - self.width_adjustment
        )
        self.native.styles.height = (
            self.scale_in_horizontal(height) - self.height_adjustment
        )

        # Apply margins to the widget based on content spacing.
        # self.native.styles.margin = (
        #     self.scale_in_vertical(self.interface.layout.content_top),
        #     self.scale_in_horizontal(self.interface.layout.content_right),
        #     self.scale_in_vertical(self.interface.layout.content_bottom),
        #     self.scale_in_horizontal(self.interface.layout.content_left),
        # )

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
        self.native.mount(child.native)

    def insert_child(self, index, child):
        pass

    def remove_child(self, child):
        self.native.remove(child.native)

    def refresh(self):
        intrinsic = self.interface.intrinsic
        intrinsic.width = intrinsic.height = None
        self.rehint()
        assert intrinsic.width is not None
        assert intrinsic.height is not None

        intrinsic.width = self.scale_out_horizontal(intrinsic.width)
        intrinsic.height = self.scale_out_vertical(intrinsic.height)
