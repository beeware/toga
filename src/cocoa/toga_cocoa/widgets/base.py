from toga_cocoa.libs import NSColor, NSColorUsingColorName

from ..container import Constraints


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
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        if self.constraints and self.native:
            self._container.native.addSubview_(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container
        self.interface.rehint()

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def add_constraints(self):
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.constraints = Constraints(self)

    def apply_layout(self):
        if self.constraints:
            self.constraints.update()

    def set_font(self, font):
        self.native.setFont_(font.native)

    def set_enabled(self, value):
        self.native.setEnabled_(value)

    def set_background_color(self, background_color):
        if background_color:
            if isinstance(background_color, tuple):
                background_color = NSColor.colorWithRed_green_blue_alpha_(background_color[0] / 255,
                                                                          background_color[1] / 255,
                                                                          background_color[2] / 255, 1.0)
            elif isinstance(background_color, str):
                try:
                    background_color = NSColorUsingColorName(background_color.upper())
                except:
                    raise ValueError(
                        'Background color %s does not exist, try a RGB number (red, green, blue).' % background_color)
            else:
                raise ValueError('_set_background_color on button widget must receive a tuple or a string')

            self.native.setBordered_(False)
            self.native.setWantsLayer_(True)
            self.native.setBackgroundColor_(background_color)

    def rehint(self):
        pass
