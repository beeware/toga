from toga_dummy.utils import not_required_on, LoggedObject


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

    def update(self):
        pass

    @property
    def width(self):
        pass

    @width.setter
    def width(self, value):
        pass

    @property
    def height(self):
        pass

    @height.setter
    def height(self, value):
        pass

    @property
    def left(self):
        pass

    @left.setter
    def left(self, value):
        pass

    @property
    def top(self):
        pass

    @top.setter
    def top(self, value):
        pass


class Container(LoggedObject):
    @property
    def content(self):
        return self._get_value('content')

    @content.setter
    def content(self, widget):
        self._set_value('content', widget)

    def update_layout(self, **style):
        self._action('update container layout', style=style)
