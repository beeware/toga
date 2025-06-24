from unittest.mock import Mock

from toga.constants import FlashMode
from toga_cocoa import libs as cocoa
from toga_cocoa.hardware.camera import TogaCameraWindow
from toga_cocoa.libs import (
    AVAuthorizationStatus,
    AVCaptureFlashMode,
    AVMediaTypeVideo,
)

from ..app import AppProbe


class CameraProbe(AppProbe):
    allow_no_camera = True
    request_permission_on_first_use = True

    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch

        # A mocked permissions table. The key is the media type; the value is True
        # if permission has been granted, False if it has be denied. A missing value
        # will be turned into a grant if permission is requested.
        self._mock_permissions = {}

        # Mock AVCaptureDevice
        # 2 devices installed. Camera 1 has a flash; camera 2 does not.
        self._mock_AVCaptureDevice = Mock()

        self._mock_camera_1 = Mock(uniqueID="camera-1", localizedName="Camera 1")
        self._mock_camera_1.isFlashAvailable.return_value = True

        self._mock_camera_2 = Mock(uniqueID="camera-2", localizedName="Camera 2")
        self._mock_camera_2.isFlashAvailable.return_value = False

        self._mock_AVCaptureDevice.devicesWithMediaType.return_value = [
            self._mock_camera_1,
            self._mock_camera_2,
        ]

        def _mock_auth_status(media_type):
            try:
                return {
                    1: AVAuthorizationStatus.Authorized.value,
                    0: AVAuthorizationStatus.Denied.value,
                }[self._mock_permissions[str(media_type)]]
            except KeyError:
                return AVAuthorizationStatus.NotDetermined.value

        self._mock_AVCaptureDevice.authorizationStatusForMediaType = _mock_auth_status

        def _mock_request_access(media_type, completionHandler):
            # Fire completion handler
            try:
                self._mock_permissions[str(media_type)] = abs(
                    self._mock_permissions[str(media_type)]
                )
                result = bool(self._mock_permissions[str(media_type)])
            except KeyError:
                # If there's no explicit permission, it's a denial
                self._mock_permissions[str(media_type)] = 0
                result = False
            completionHandler.func(result)

        self._mock_AVCaptureDevice.requestAccessForMediaType = _mock_request_access

        monkeypatch.setattr(cocoa, "AVCaptureDevice", self._mock_AVCaptureDevice)

        # Mock AVCaptureDeviceInput
        self._mock_AVCaptureDeviceInput = Mock()

        def _mock_deviceInput(device, error):
            return Mock(device=device)

        self._mock_AVCaptureDeviceInput.deviceInputWithDevice = _mock_deviceInput

        monkeypatch.setattr(
            cocoa, "AVCaptureDeviceInput", self._mock_AVCaptureDeviceInput
        )

        # Mock AVCapturePhotoSettings
        self._mock_AVCapturePhotoSettings = Mock()

        self._mock_photoSettings = Mock()
        self._mock_AVCapturePhotoSettings.photoSettings.return_value = (
            self._mock_photoSettings
        )

        monkeypatch.setattr(
            cocoa, "AVCapturePhotoSettings", self._mock_AVCapturePhotoSettings
        )

        # Mock creation of a camera Session
        def _mock_camera_session(window, device, flash):
            def _addInput(input):
                window.camera_session.inputs.append(input)

            def _removeInput(input):
                window.camera_session.inputs.remove(input)

            window.camera_session = Mock(
                inputs=[],
                outputs=[Mock()],
                addInput=_addInput,
                removeInput=_removeInput,
            )

            window._enable_camera(device, flash)

        monkeypatch.setattr(
            TogaCameraWindow, "create_camera_session", _mock_camera_session
        )

    def cleanup(self):
        # Ensure there are no open camrea preview windows at the end of a test.
        for window in self.app.camera._impl.preview_windows:
            window.interface.close()

    def known_cameras(self):
        return {
            "camera-1": ("Camera 1", True),
            "camera-2": ("Camera 2", False),
        }

    def select_other_camera(self):
        device = self.app.camera.devices[1]
        self.app.camera._impl.preview_windows[0].device_select.value = device
        return device

    def disconnect_cameras(self):
        self._mock_AVCaptureDevice.devicesWithMediaType.return_value = []

    def reset_permission(self):
        self._mock_permissions = {}

    def grant_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = 1

    def allow_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = -1

    def reject_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = 0

    async def wait_for_camera(self, device_count=2):
        # A short delay is needed to ensure that the window fully creates.
        await self.redraw("Camera view displayed", delay=0.1)

        # Session has been started, and there are devices
        window = self.app.camera._impl.preview_windows[0]
        window.camera_session.startRunning.assert_called_once_with()

        assert len(window.device_select.items) == device_count

    @property
    def shutter_enabled(self):
        return self.app.camera._impl.preview_windows[0].shutter_button.enabled

    async def press_shutter_button(self, photo):
        window = self.app.camera._impl.preview_windows[0]
        device_used = window.camera_session.inputs[0].device
        # The shutter button should be enabled
        assert self.shutter_enabled

        # Press the shutter button
        window.take_photo(None)
        await self.redraw("Shutter pressed")

        # Photo settings were created with the right flash mode
        self._mock_AVCapturePhotoSettings.photoSettings.assert_called_once_with()
        self._mock_AVCapturePhotoSettings.photoSettings.reset_mock()
        flash_mode = self._mock_photoSettings.flashMode

        # The capture mechanism was invoked
        output = window.camera_session.outputs[0]
        output.capturePhotoWithSettings.assert_called_once_with(
            self._mock_photoSettings,
            delegate=window.camera_session,
        )
        output.capturePhotoWithSettings.reset_mock()

        # Fake the result of a successful photo being taken
        image_data = (self.app.paths.app / "resources/photo.png").read_bytes()

        result = Mock()
        result.fileDataRepresentation.return_value = Mock(
            bytes=image_data, length=len(image_data)
        )

        window.photo_taken(result)

        # The window has been closed and the session ended
        assert window.closed
        window.camera_session.stopRunning.assert_called_once_with()
        window.camera_session.stopRunning.reset_mock()
        assert window not in self.app.camera._impl.preview_windows

        return await photo, device_used, flash_mode

    async def cancel_photo(self, photo):
        window = self.app.camera._impl.preview_windows[0]

        # Trigger a user close of the camera window
        window.on_close()
        await self.redraw("Photo cancelled")

        # The window has been closed and the session ended
        assert window.closed
        window.camera_session.stopRunning.assert_called_once_with()
        assert window not in self.app.camera._impl.preview_windows

        return await photo

    def same_device(self, device, native):
        if device is None:
            return self._mock_camera_1 == native
        else:
            return device._impl.native == native

    def same_flash_mode(self, expected, actual):
        return (
            expected
            == {
                AVCaptureFlashMode.Auto: FlashMode.AUTO,
                AVCaptureFlashMode.On: FlashMode.ON,
                AVCaptureFlashMode.Off: FlashMode.OFF,
            }[actual]
        )
