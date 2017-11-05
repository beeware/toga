from ..utils import not_required, not_required_on, LogEntry, LoggedObject


class Widget(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self.create()

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

    @property
    def enabled(self):
        return self._get_value('enabled')

    @enabled.setter
    def enabled(self, value):
        self._set_value('enabled', value)

    def add_child(self, child):
        self._action('add child', child=child)

    @not_required_on('gtk', 'winforms', 'android', 'web')
    def add_constraints(self):
        self._action('add constraints')

    def apply_layout(self):
        self._action('apply layout')

    def apply_sub_layout(self):
        self._action('apply sub layout')

    def set_font(self, font):
        self._set_value('font', font)

    def rehint(self):
        self._action('rehint')
