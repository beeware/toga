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

    def make_root(self):
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


class Container:
    def __init__(self):
        pass

    @property
    def content(self):
        pass

    @content.setter
    def content(self, widget):
        pass

    @property
    def root_content(self):
        pass

    @root_content.setter
    def root_content(self, widget):
        pass

    def update_layout(self, **style):
        pass
