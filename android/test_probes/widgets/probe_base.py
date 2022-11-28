from pytest import skip


class SimpleProbe:
    def __init__(self, main_box, widget):
        native_box = main_box._impl.native
        assert native_box.getChildCount == 1
        self.native = native_box.getChildAt[0]
        assert isinstance(self.native, self.native_class)

        # Although this isn't part of the public API, we often point users at it to do
        # things that Toga itself doesn't support.
        assert widget._impl.native is self.native

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
