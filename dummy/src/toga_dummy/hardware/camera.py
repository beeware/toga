from ..utils import LoggedObject


class CameraDevice:
    def __init__(self, id, name, has_flash):
        self._id = id
        self._name = name
        self._has_flash = has_flash

    def id(self):
        return self._id

    def name(self):
        return self._name

    def has_flash(self):
        return self._has_flash


class Camera(LoggedObject):
    CAMERA_1 = CameraDevice(id="camera-1", name="Camera 1", has_flash=True)
    CAMERA_2 = CameraDevice(id="camera-2", name="Camera 2", has_flash=False)

    def __init__(self, interface):
        self.interface = interface

        # -1: permission *could* be granted, but hasn't been
        # 1: permission has been granted
        # 0: permission has been denied, or can't be granted
        self._has_permission = -1

    def has_permission(self, allow_unknown=False):
        self._action("has permission")
        if allow_unknown:
            return abs(self._has_permission)
        else:
            return self._has_permission > 0

    def request_permission(self, future):
        self._action("request permission")
        self._has_permission = abs(self._has_permission)
        future.set_result(self._has_permission != 0)

    def get_devices(self):
        self._action("get devices")
        return [self.CAMERA_1, self.CAMERA_2]

    def take_photo(self, future, device, flash):
        if self.has_permission(allow_unknown=True):
            self._action(
                "take photo",
                permission_requested=self._has_permission < 0,
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
