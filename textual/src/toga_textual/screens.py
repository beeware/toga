from toga.screens import Screen as ScreenInterface

from .widgets.base import Scalable


class Screen(Scalable):
    _instances = {}

    def __new__(cls, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native] = instance
            return instance

    def get_name(self):
        return "Textual Screen"

    def get_origin(self):
        return (0, 0)

    def get_size(self):
        return (
            self.scale_out_horizontal(self.native.size.width),
            self.scale_out_vertical(self.native.size.height),
        )

    def get_image_data(self):
        self.interface.factory.not_implemented("Screen.get_image_data()")
