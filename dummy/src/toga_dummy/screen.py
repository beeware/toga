from toga.screen import Screen as ScreenInterface

from .utils import LoggedObject, not_required, not_required_on  # noqa


@not_required_on("mobile", "web")
class Screen(LoggedObject):
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
        return self.native

    def get_origin(self):
        if self.native == "primary_screen":
            return (0, 0)
        else:
            return (-1920, 0)
