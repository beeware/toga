from toga.screen import Screen as ScreenInterface

from .widgets.base import Scalable


class Screen(Scalable):
    _instances = {}

    def __new__(cls, app, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native] = instance
            cls.app = app
            instance.init_scale(instance.app.native)
            return instance

    def get_name(self) -> str:
        return str(self.native.getName())

    def get_origin(self) -> tuple[int, int]:
        return (0, 0)

    def get_size(self) -> tuple[int, int]:
        return (
            self.scale_out(self.native.getWidth()),
            self.scale_out(self.native.getHeight()),
        )

    def get_image_data(self):
        self.interface.factory.not_implemented("Screen.get_image_data()")
