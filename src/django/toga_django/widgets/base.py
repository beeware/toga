
class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.create()

    def handler(self, fn, name):
        if hasattr(fn, '__self__'):
            ref = '(%s,%s-%s)' % (fn.__self__.id, self.id, name)
        else:
            ref = '%s-%s' % (self.id, name)

        return ref

    @property
    def ports(self):
        return ",".join(
            "%s=%s" % (name, widget.id)
            for name, widget in self.__dict__.items()
            if isinstance(widget, Widget)
        )

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

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        # No implementation required here; the new sizing will be picked up
        # by the box's allocation handler.
        pass

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


    ### INTERFACE

    def add_child(self, child):
        pass
        # if self._container:
            # child._set_container(self._container)

    def rehint(self):
        pass

    def set_font(self, font):
        self.interface.factory.not_implemented('Widget.set_font()')
