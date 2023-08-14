import os

from toga.screen import Screen as ScreenInterface

from .libs import Gdk


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
        return self.native.get_model()

    def get_origin(self):
        geometry = self.native.get_geometry()
        return geometry.x, geometry.y

    def get_size(self):
        geometry = self.native.get_geometry()
        return geometry.width, geometry.height

    def get_image_data(self):
        def get_image_data(self):
            if os.environ.get("XDG_SESSION_TYPE", "").lower() == "x11":
                # Only works for x11
                display = self.native.get_display()
                screen = display.get_default_screen()
                window = screen.get_root_window()
                geometry = self.native.get_geometry()
                screenshot = Gdk.pixbuf_get_from_window(
                    window, geometry.x, geometry.y, geometry.width, geometry.height
                )
                success, buffer = screenshot.save_to_bufferv("png", [], [])
                if success:
                    return bytes(buffer)
                else:
                    print("Failed to save screenshot to buffer.")
                    return None
            else:
                # Not implemented for wayland
                self.interface.factory.not_implemented("Screen.get_image_data()")
                return None
