from toga.hardware.camera import Device as TogaDevice

from ..utils import LoggedObject


class Camera(LoggedObject):
    CAMERA_1 = TogaDevice(id="camera-1", name="Camera 1", native=object())
    CAMERA_2 = TogaDevice(id="camera-2", name="Camera 2", native=object())

    def __init__(self, interface):
        self.interface = interface

        # -1: permission *could* be granted, but hasn't been
        # 1: permission has been granted
        # 0: permission has been denied, or can't be granted
        self._has_photo_permission = -1

    def has_photo_permission(self, allow_unknown=False):
        self._action("has photo permission")
        if allow_unknown:
            return abs(self._has_photo_permission)
        else:
            return self._has_photo_permission > 0

    def request_photo_permission(self, future):
        self._action("request photo permission")
        self._has_photo_permission = abs(self._has_photo_permission)
        future.set_result(self._has_photo_permission != 0)

    def get_devices(self):
        self._action("get devices")
        return [self.CAMERA_1, self.CAMERA_2]

    def has_flash(self, device):
        self._action("has flash", device=device)
        # Camera 1 has a flash; camera 2 doesn't.
        return device.id == "camera-1"

    def take_photo(self, future, device, flash):
        if self.has_photo_permission(allow_unknown=True):
            self._action(
                "take photo",
                permission_requested=self._has_photo_permission < 0,
                device=device,
                flash=flash,
            )

            # Requires that the user has first called `simulate_photo()` with the
            # photo to be captured.
            future.set_result(self._photo)
            del self._photo
        else:
            raise PermissionError("App does not have permission to take photos")

    def simulate_photo(self, image):
        self._photo = image
