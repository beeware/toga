
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

    def set_container(self, container):
        # if self._constraints and self._impl:
            # self._container._impl.addSubview_(self._impl)
            # self._constraints._container = container
        self.rehint()

    def add_child(self, child):
        pass
        # if self._container:
            # child._set_container(self._container)

    def apply_layout(self):
        pass
        # if self._constraints:
        #     self._constraints.update()

    def apply_sub_layout(self):
        pass
        # if self._constraints:
        #     self._constraints.update()

    def rehint(self):
        pass

    def set_font(self, font):
        raise NotImplementedError()

    @property
    def enabled(self):
        raise NotImplementedError()

    @enabled.setter
    def enabled(self, value):
        raise NotImplementedError()

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
