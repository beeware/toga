from toga.screen import Screen as ScreenInterface


class Screen:
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
        return self.native.localizedName

    def get_origin(self):
        frame_native = self.native.frame()
        return (
            frame_native.origin.x,
            frame_native.origin.y + frame_native.size.height,
        )
