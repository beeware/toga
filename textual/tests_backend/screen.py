from textual.screen import Screen as TextualScreen


class ScreenProbe:
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self._impl = screen._impl
        self.native = screen._impl.native
        assert isinstance(self.native, TextualScreen)

    def assert_name(self):
        assert self.screen.name == "Textual Screen"

    def assert_origin(self):
        assert self.screen.origin == (0, 0)

    def assert_size(self):
        assert self.screen.size == (self.native.size.width, self.native.size.height)
