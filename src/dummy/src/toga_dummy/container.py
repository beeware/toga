from toga_dummy.utils import not_required_on


@not_required_on('gtk', 'winforms', 'android', 'web')
class Constraints:
    def __init__(self, widget):
        pass

    @property
    def widget(self):
        pass

    @widget.setter
    def widget(self, value):
        pass

    @property
    def container(self):
        pass

    @container.setter
    def container(self, value):
        pass

    def update(self, x, y, width, height):
        pass
