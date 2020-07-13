from .base import Widget


class Box(Widget):
    def __html__(self):
        return """
        <button>{self.interface.label}</button>
        """.format(self=self)

    def create(self):
        pass

    def add_child(self, child):
        pass
