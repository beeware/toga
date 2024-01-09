from unittest.mock import Mock

from toga_cocoa import libs as cocoa
from toga_cocoa.hardware.camera import TogaCameraWindow
from toga_cocoa.libs import (
    AVAuthorizationStatus,
    AVMediaTypeVideo,
)

from ..app import AppProbe


class CameraProbe(AppProbe):
    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch

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
                    -1: AVAuthorizationStatus.NotDetermined.value,
                }[self._mock_permissions[str(media_type)]]
            except KeyError:
                return AVAuthorizationStatus.NotDetermined.value

        self._mock_AVCaptureDevice.authorizationStatusForMediaType = _mock_auth_status

        def _mock_request_access(media_type, completionHandler):
            # Fire completion handler
            try:
                # Convert an "allow" in to a full grant.
                if self._mock_permissions[str(media_type)] == -1:
                    self._mock_permissions[str(media_type)] = 1

                result = self._mock_permissions[str(media_type)]
            except KeyError:
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

    def known_cameras(self):
        return {
            "camera-1": True,
            "camera-2": False,
        }

    def select_other_camera(self):
        device = self.app.camera.devices[1]
        self.app.camera._impl.preview_windows[0].device_select.value = device
        return device

    def disconnect_cameras(self):
        self._mock_AVCaptureDevice.devicesWithMediaType.return_value = []

    def reset_photo_permission(self):
        self._mock_permissions = {}

    def allow_photo_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = -1

    def reject_photo_permission(self):
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
        assert window not in self.app.camera._impl.preview_windows

        return await photo, device_used

    async def cancel_photo(self, photo):
        window = self.app.camera._impl.preview_windows[0]

        # Close the camera window.
        window._impl.cocoa_windowShouldClose()
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
            return device._native == native
