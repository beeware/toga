import warnings
from pathlib import Path

from android.content import Context, Intent
from android.content.pm import PackageManager
from android.hardware.camera2 import CameraCharacteristics
from android.provider import MediaStore
from androidx.core.content import FileProvider
from java.io import File

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

    def has_permission(self):
        result = self.interface.app._impl._native_checkSelfPermission(
            Camera.CAMERA_PERMISSION
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
            # We have permission; go directly to taking the photo.
            # The "shared" subfolder of the app's cache folder is
            # marked as a file provider. Ensure the folder exists.
            shared_folder = File(self.context.getCacheDir(), "shared")
            if not shared_folder.exists():
                shared_folder.mkdirs()

            # Create a temporary file in the shared folder,
            # and convert it to a URI using the app's fileprovider.
            photo_file = File.createTempFile("camera", ".jpg", shared_folder)
            photo_uri = FileProvider.getUriForFile(
                self.context,
                f"{self.interface.app.app_id}.fileprovider",
                photo_file,
            )

            def photo_taken(code, data):
                # Activity.RESULT_CANCELED == 0
                if code:
                    photo = toga.Image(Path(photo_file.getAbsolutePath()))
                    result.set_result(photo)
                else:
                    result.set_result(None)

            intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            intent.putExtra(MediaStore.EXTRA_OUTPUT, photo_uri)
            self.interface.app._impl.start_activity(intent, on_complete=photo_taken)
        else:
            raise PermissionError("App does not have permission to take photos")
