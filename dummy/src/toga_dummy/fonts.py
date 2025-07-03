from toga.fonts import UnknownFontError

from .utils import LoggedObject


class Font(LoggedObject):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def load_predefined_system_font(self):
        if self.interface.family not in {
            "system",
            "message",
            "serif",
            "sans-serif",
            "cursive",
            "fantasy",
            "monospace",
        }:
            raise UnknownFontError

    def load_user_registered_font(self):
        if self.interface.family == "Bogus Font":
            raise UnknownFontError(f"Unknown font '{self.interface}'")

    def load_arbitrary_system_font(self):
        raise UnknownFontError

    def __eq__(self, other):
        return all(
            [
                self.interface.family == other.interface.family,
                self.interface.size == other.interface.size,
                self.interface.weight == other.interface.weight,
                self.interface.variant == other.interface.variant,
                self.interface.style == other.interface.style,
            ]
        )
