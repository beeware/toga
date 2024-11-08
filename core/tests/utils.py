import toga
from toga.platform import get_platform_factory


# Create the simplest possible widget with a concrete implementation that will
# allow children
class ExampleWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        self.factory = get_platform_factory()
        self._impl = self.factory.Widget(self)

        super().__init__(*args, **kwargs)

        self._children = []

    def __repr__(self):
        return f"Widget(id={self.id!r})"


# Create the simplest possible widget with a concrete implementation that cannot
# have children.
class ExampleLeafWidget(toga.Widget):
    def __init__(self, *args, **kwargs):
        self.factory = get_platform_factory()
        self._impl = self.factory.Widget(self)

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Widget(id={self.id!r})"
