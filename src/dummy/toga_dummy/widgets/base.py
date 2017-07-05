class Widget():
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        pass

    @container.setter
    def container(self, container):
        pass

    def add_child(self, child):
        pass

    def add_constraints(self):
        pass

    def apply_layout(self):
        pass

    def set_font(self, font):
        pass

    def set_enabled(self, value):
        pass

    def rehint(self):
        pass