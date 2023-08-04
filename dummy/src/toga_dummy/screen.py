from .utils import LoggedObject, not_required, not_required_on  # noqa


@not_required_on("mobile", "web")
class Screen(LoggedObject):
    _instances = {}

    def __new__(cls, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = None
            instance.native = native
            cls._instances[native] = instance
            return instance

    def get_name(self):
        self._get_value("ScreenName")

    def get_origin(self):
        self._get_value("origin", (0, 0))
