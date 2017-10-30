
class Container:
    def __init__(self):
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content._container = self

    @property
    def root_content(self):
        return self._content

    @root_content.setter
    def root_content(self, widget):
        self._content = widget
        self._content._container = self
        # Make the constraints object a root container.
        self._constraints.make_root()

    def update_layout(self, **style):
        pass
