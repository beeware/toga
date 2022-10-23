from ..utils import LoggedObject, not_required_on


class Widget(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self.viewport = None
        self.create()

    def create(self):
        pass

    def set_app(self, app):
        self._set_value('app', app)

    def set_window(self, window):
        self._set_value('window', window)

    @property
    def container(self):
        return self._get_value('container')

    @container.setter
    def container(self, container):
        self._set_value('container', container)

    def set_enabled(self, value):
        self._action('set enabled', value=value)

    def focus(self):
        self._action('focus')

    ######################################################################
    # APPLICATOR
    ######################################################################

    def set_bounds(self, x, y, width, height):
        self._action('set bounds', x=x, y=y, width=width, height=height)

    def set_hidden(self, hidden):
        self._action('set hidden', hidden=hidden)

    def set_font(self, font):
        self._action('set font', font=font)

    def set_background_color(self, color):
        self._action('set background color', color=color)

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        self._action('add child', child=child)

    def insert_child(self, index, child):
        self._action('insert child', index=index, child=child)

    def remove_child(self, child):
        self._action('remove child', child=child)

    @not_required_on('gtk', 'winforms', 'android', 'web')
    def add_constraints(self):
        self._action('add constraints')

    def rehint(self):
        self._action('rehint')
