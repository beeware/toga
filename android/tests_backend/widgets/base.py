from pytest import skip


class SimpleProbe:
    def __init__(self, widget, container):
        for i in range(container._impl.native.getChildCount()):
            child = container._impl.native.getChildAt(i)
            if child is widget._impl.native:
                self.native = child
                assert isinstance(self.native, self.native_class)
                break
        else:
            raise ValueError(f"cannot find {widget} in {container}")

    @property
    def enabled(self):
        return self.native.isEnabled()

    @property
    def background_color(self):
        skip("not implemented: background_color")

    @property
    def color(self):
        skip("not implemented: color")

    @property
    def hidden(self):
        skip("not implemented: hidden")

    @property
    def width(self):
        return self.native.getWidth()

    @property
    def height(self):
        return self.native.getHeight()

    def press(self):
        self.native.performClick()
