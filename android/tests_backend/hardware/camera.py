import shutil
from unittest.mock import Mock

import pytest
from android.provider import MediaStore

from toga_android.hardware.camera import Camera

from .hardware import HardwareProbe


class CameraProbe(HardwareProbe):
    allow_no_camera = False
    request_permission_on_first_use = False

    def cleanup(self):
        # Ensure that after a test runs, there's no shared files.
        shutil.rmtree(self.app.paths.cache / "shared", ignore_errors=True)

    def known_cameras(self):
        # The Android emulator has a single camera. Physical devices will have other
        # properties, this test result won't be accurate.
        return {
            "1": ("Camera 1", True),
        }

    def select_other_camera(self):
        pytest.xfail("Android can't programmatically select other cameras")

    def disconnect_cameras(self):
        # native=False
        self.app.camera._impl.has_camera = False

    def reset_permission(self):
        self._mock_permissions = {}

    def grant_permission(self):
        self._mock_permissions[Camera.CAMERA_PERMISSION] = 1

    def allow_permission(self):
        self._mock_permissions[Camera.CAMERA_PERMISSION] = -1

    def reject_permission(self):
        self._mock_permissions[Camera.CAMERA_PERMISSION] = 0

    async def wait_for_camera(self, device_count=0):
        await self.redraw("Camera view displayed")

    @property
    def shutter_enabled(self):
        # Shutter can't be disabled
        return True

    async def press_shutter_button(self, photo):
        # The activity was started
        self._mock_startActivityForResult.assert_called_once()
        (intent, code), _ = self._mock_startActivityForResult.call_args
        assert intent.getAction() == MediaStore.ACTION_IMAGE_CAPTURE
        self._mock_startActivityForResult.reset_mock()

        # Fake the result of a successful photo being taken.
        output_uri = intent.getExtras().get(MediaStore.EXTRA_OUTPUT)
        shared_suffix = output_uri.getPath()[1:]

        # The shared folder *must* exist as a result of the camera being triggered.
        assert (self.app.paths.cache / shared_suffix).parent.is_dir()
        # Copy the reference file to the location that the camera intent would have
        # populated.
        shutil.copy(
            self.app.paths.app / "resources/photo.png",
            self.app.paths.cache / shared_suffix,
        )
        data = Mock()
        # Activity.RESULT_OK = -1
        self.app._impl._listener.onActivityResult(code, -1, data)

        await self.redraw("Photo taken")

        return await photo, None, None

    async def cancel_photo(self, photo):
        # The activity was started
        self._mock_startActivityForResult.assert_called_once()
        (intent, code), _ = self._mock_startActivityForResult.call_args
        assert intent.getAction() == MediaStore.ACTION_IMAGE_CAPTURE
        self._mock_startActivityForResult.reset_mock()

        # Fake the result of a cancelled photo.
        data = Mock()
        # Activity.RESULT_CANCELLED = 0
        self.app._impl._listener.onActivityResult(code, 0, data)

        await self.redraw("Photo cancelled")

        return await photo

    def same_device(self, device, native):
        # Android provides no real camera control; so return all devices as a match
        return True

    def same_flash_mode(self, expected, actual):
        # Android provides no real camera control; so return all devices as a match
        return True
