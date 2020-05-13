from ..libs.activity import MainActivity


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.native = None
        # Capture a reference to the Java `MainActivity` instance, so that subclasses
        # can pass it as `context` when creating native Android widgets.
        self._native_activity = MainActivity.singletonThis
        self.create()

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
        self.viewport = container.viewport

        if self.native:
            # When initially setting the container and adding widgets to the container,
            # we provide no `LayoutParams`. Those are promptly added when Toga
            # calls `widget.rehint()` and `widget.set_bounds()`.
            self._container.native.addView(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.setEnabled(value)

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        if self.container:
            # Ask the container widget to set our bounds.
            self.container.set_child_bounds(self, x, y, width, height)

    def set_hidden(self, hidden):
        self.interface.factory.not_implemented("Widget.set_hidden()")

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed.
        pass

    # INTERFACE

    def add_child(self, child):
        if self.container:
            child.viewport = self.root.viewport
            child.container = self.container

    def rehint(self):
        pass
