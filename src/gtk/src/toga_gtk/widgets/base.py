from travertino.size import at_least

from ..libs import (
    apply_gtk_style,
    get_color_css,
    get_bg_color_css,
    get_font_css
)


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.viewport = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    def create(self):
        pass

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            if container:
                raise RuntimeError('Already have a container')
            else:
                # container is set to None, removing self from the container.native
                # Note from pygtk documentation: Note that the container will own a
                # reference to widget, and that this may be the last reference held;
                # so removing a widget from its container can cause that widget to be
                # destroyed. If you want to use widget again, you should add a
                # reference to it.
                self._container.native.remove(self.native)
                self._container = None
        elif container:
            # setting container, adding self to container.native
            self._container = container
            self._container.native.add(self.native)
            self.native.show_all()

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(self.interface.enabled)

    def focus(self):
        self.native.grab_focus()

    ######################################################################
    # APPLICATOR
    ######################################################################

    def set_bounds(self, x, y, width, height):
        # No implementation required here; the new sizing will be picked up
        # by the box's allocation handler.
        pass

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        return not self.native.set_visible(not hidden)

    def set_color(self, color):
        if color:
            style_context = self.native.get_style_context()
            css = get_color_css(color)
            apply_gtk_style(style_context, css, "toga-color")

    def set_background_color(self, color):
        if color:
            style_context = self.native.get_style_context()
            css = get_bg_color_css(color)
            apply_gtk_style(style_context, css, "toga-bg-color")

    def set_font(self, font):
        if font:
            style_context = self.native.get_style_context()
            css = get_font_css(font)
            apply_gtk_style(style_context, css, "toga-font")

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        if self.viewport:
            # we are the the top level container
            child.container = self
        else:
            child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = at_least(height[0])
