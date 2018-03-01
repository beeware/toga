from toga_winforms.libs import Point, Size


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        if self.native:
            self._container.native.Controls.Add(self.native)
            self.native.BringToFront()

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.interface.factory.not_implemented('Widget.set_enabled()')

    ### APPLICATOR

    @property
    def vertical_shift(self):
        return 0

    def set_bounds(self, x, y, width, height):
        if self.native:
            # Root level widgets may require vertical adjustment to
            # account for toolbars, etc.
            if self.interface.parent is None:
                vertical_shift = self.frame.vertical_shift
            else:
                vertical_shift = 0

            self.native.Size = Size(width, height)
            self.native.Location = Point(x, y + vertical_shift)

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        if self.native:
            self.native.Visible = not hidden

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_color(self, color):
        # By default, color can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed.
        pass

    ### INTERFACE

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def rehint(self):
        pass
