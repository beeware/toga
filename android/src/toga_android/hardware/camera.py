import warnings

from android.content import Context, Intent
from android.content.pm import PackageManager
from android.hardware.camera2 import CameraCharacteristics
from android.provider import MediaStore
from androidx.core.content import ContextCompat

import toga


class CameraDevice:
    def __init__(self, manager, id):
        self._manager = manager
        self._id = id

    def id(self):
        return self._id

    def name(self):
        return f"Camera {self._id}"

    def has_flash(self):
        characteristics = self._manager.getCameraCharacteristics(self._id)
        return characteristics.get(CameraCharacteristics.FLASH_INFO_AVAILABLE)


class Camera:
    CAMERA_PERMISSION = "android.permission.CAMERA"

    def __init__(self, interface):
        self.interface = interface

        # Does the device have a camera?
        self.context = self.interface.app._impl.native.getApplicationContext()
        self.has_camera = self.context.getPackageManager().hasSystemFeature(
            PackageManager.FEATURE_CAMERA
        )

    def _native_checkSelfPermission(self, context, permission):  # pragma: no cover
        # A wrapper around the native call so it can be mocked.
        return ContextCompat.checkSelfPermission(context, Camera.CAMERA_PERMISSION)

    def has_permission(self):
        result = self._native_checkSelfPermission(
            self.context, Camera.CAMERA_PERMISSION
        )
        return result == PackageManager.PERMISSION_GRANTED

    def request_permission(self, future):
        def request_complete(permissions, results):
            # Map the permissions to their result
            perms = dict(zip(permissions, results))
            try:
                result = (
                    perms[Camera.CAMERA_PERMISSION] == PackageManager.PERMISSION_GRANTED
                )
            except KeyError:  # pragma: no cover
                # This shouldn't ever happen - we shouldn't get a completion of a camera
                # permission request that doesn't include the camera permission - but
                # just in case, we'll assume if it's not there, it failed.
                result = False
            future.set_result(result)

        self.interface.app._impl.request_permissions(
            [Camera.CAMERA_PERMISSION],
            on_complete=request_complete,
        )

    def get_devices(self):
        manager = self.interface.app._impl.native.getSystemService(
            Context.CAMERA_SERVICE
        )

        return [
            CameraDevice(manager=manager, id=ident)
            for ident in manager.getCameraIdList()
        ]

    def take_photo(self, result, device, flash):
        if not self.has_camera:
            warnings.warn("No camera is available")
            result.set_result(None)
        elif self.has_permission():
            # We have permission; go directly to taking the photo
            def photo_taken(code, data):
                # Activity.RESULT_CANCELED == 0
                if code:
                    bundle = data.getExtras()
                    bitmap = bundle.get("data")
                    thumb = toga.Image(bitmap)
                    result.set_result(thumb)
                else:
                    result.set_result(None)

            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            # TODO: The image returned by default is only a thumbnail. There's some sort
            # of jiggery-pokery needed to return an actual image.
            # intent.putExtra(MediaStore.EXTRA_OUTPUT, ...)
            self.interface.app._impl.start_activity(intent, on_complete=photo_taken)
        else:
            raise PermissionError("App does not have permission to take photos")
