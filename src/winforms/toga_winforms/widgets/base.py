from toga_winforms.libs import *


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.constraints = None
        self.native = None
        self.create()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def enabled(self):
        raise NotImplmementedError()

    @enabled.setter
    def enabled(self, value):
        raise NotImplmementedError()

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        if self.native:
            self._container.native.Controls.Add(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.interface.rehint()

    def add_child(self, child):
        if self.container:
            child._set_container(self.container)

    def apply_layout(self):
        if self.native:
            self.native.Size = Size(int(self.interface.layout.width), int(self.interface.layout.height))
            self.native.Location = Point(int(self.interface.layout.absolute.left), int(self.interface.layout.absolute.top))

    def apply_sub_layout(self):
        # If widget have sub layouts like the ScrollContainer or SplitView,                                                                                                                                                                                                                                                                                                                                     update them.
        pass

    def rehint(self):
        pass

    def set_font(self, font):
        pass
