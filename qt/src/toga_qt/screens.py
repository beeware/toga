from PySide6.QtCore import QBuffer, QByteArray, QIODevice

from toga.screens import Screen as ScreenInterface
from toga.types import Position, Size

from .libs import IS_WAYLAND


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
        # FIXME:  What combinations of values are guaranteed to be
        # unique?
        return "|".join(
            [
                self.native.name(),
                self.native.model(),
                self.native.manufacturer(),
                self.native.serialNumber(),
            ]
        )

    def get_origin(self) -> Position:
        return Position(
            self.native.geometry().topLeft().x(), self.native.geometry().topLeft().y()
        )

    def get_size(self) -> Size:
        geometry = self.native.geometry()
        return Size(geometry.width(), geometry.height())

    def get_image_data(self):
        if not IS_WAYLAND:  # pragma: no-cover-if-linux-wayland
            grabbed = self.native.grabWindow(0)
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            grabbed.save(buffer, "PNG")
            return byte_array.data()
        else:  # pragma: no-cover-if-linux-x
            self.interface.factory.not_implemented("Screen.get_image_data() on Wayland")
