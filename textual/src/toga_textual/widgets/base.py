class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
        self.create()

    @property
    def viewport(self):
        return self.container

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

    def set_bounds(self, x, y, width, height):
        pass
        # self.native.styles.width = width
        # self.native.styles.height = height

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
        pass

    def mount(self, parent):
        parent.native.mount(self.native)
        for child in self.interface.children:
            child._impl.mount(self)
