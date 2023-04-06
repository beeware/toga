from .utils import LoggedObject


class Font(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def measure(self, text, dpi, tight):
        # This isn't a real font sizing calculation;
        # it assumes all characters have an equal width.
        if tight:
            return int(len(text) * dpi / 60)
        return int(len(text) * dpi / 50)
