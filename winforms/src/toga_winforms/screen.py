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
        return self.native.DeviceName

    def get_origin(self):
        return self.native.Bounds.X, self.native.Bounds.Y

    def get_size(self):
        return self.native.Bounds.Width, self.native.Bounds.Height
