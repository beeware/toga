from .utils import LoggedObject, not_required, not_required_on


class Window(LoggedObject):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self.interface = interface

        self.set_title(title)
        self.set_position(position)
        self.set_size(size)

    def create_toolbar(self):
        self._action('create toolbar')

    def clear_content(self):
        self._action('clear content')

    def set_content(self, widget):
        self._action('set content', widget=widget)

    def get_title(self):
        return self._get_value('title')

    def set_title(self, title):
        self._set_value('title', title)

    def get_position(self):
        return self._get_value('position')

    def set_position(self, position):
        self._set_value('position', position)

    def get_size(self):
        return self._get_value('size')

    def set_size(self, size):
        self._set_value('size', size)

    def set_app(self, app):
        self._set_value('app', app)

    def show(self):
        self._action('show')
        self._set_value('visible', True)

    def hide(self):
        self._action('hide')
        self._set_value('visible', False)

    def get_visible(self):
        return self._get_value('visible')

    def close(self):
        self._action('close')

    @not_required_on('mobile')
    def set_full_screen(self, is_full_screen):
        self._set_value('is_full_screen', is_full_screen)

    @not_required
    def toga_on_close(self):
        self._action('handle Window on_close')

    @not_required_on('mobile')
    def set_on_close(self, handler):
        self._set_value('on_close', handler)
