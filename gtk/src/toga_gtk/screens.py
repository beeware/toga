from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size

from .libs import IS_WAYLAND, Gdk


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

    def get_origin(self) -> Position:
        geometry = self.native.get_geometry()
        return Position(geometry.x, geometry.y)

    def get_size(self) -> Size:
        geometry = self.native.get_geometry()
        return Size(geometry.width, geometry.height)

    def get_image_data(self):
        if IS_WAYLAND:  # pragma: no cover
            # Not implemented on wayland due to wayland security policies.
            self.interface.factory.not_implemented("Screen.get_image_data() on Wayland")
        else:  # pragma: no-cover-if-linux-wayland
            # Only works for Xorg
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
            else:  # pragma: no cover
                print("Failed to save screenshot to buffer.")
                return None
