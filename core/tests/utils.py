import toga


# Create the simplest possible widget with a concrete implementation that will
# allow children
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._children = []

    def _create(self):
        return self.factory.Widget(interface=self)

    def __repr__(self):
        return f"Widget(id={self.id!r})"


# Create the simplest possible widget with a concrete implementation that cannot
# have children.
class ExampleLeafWidget(toga.Widget):
    def _create(self):
        return self.factory.Widget(interface=self)

    def __repr__(self):
        return f"Widget(id={self.id!r})"
