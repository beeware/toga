from unittest.mock import Mock

import toga
from toga.constants import FlashMode
from toga_iOS import libs as iOS
from toga_iOS.hardware.camera import Camera
from toga_iOS.libs import (
    AVAuthorizationStatus,
    AVMediaTypeVideo,
    UIImagePickerControllerCameraCaptureMode,
    UIImagePickerControllerCameraDevice,
    UIImagePickerControllerCameraFlashMode,
    UIImagePickerControllerSourceTypeCamera,
    UIViewController,
)

from ..app import AppProbe


class CameraProbe(AppProbe):
    allow_no_camera = False
    request_permission_on_first_use = True

    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch

        # A mocked permissions table. The key is the media type; the value is True
        # if permission has been granted, False if it has be denied. A missing value
        # will be turned into a grant if permission is requested.
        self._mock_permissions = {}

        # Mock AVCaptureDevice
        self._mock_AVCaptureDevice = Mock()

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
                result = bool(self._mock_permissions[str(media_type)])
            except KeyError:
                # If there's no explicit permission, it's a denial
                self._mock_permissions[str(media_type)] = 0
                result = False
            completionHandler.func(result)

        self._mock_AVCaptureDevice.requestAccessForMediaType = _mock_request_access

        monkeypatch.setattr(iOS, "AVCaptureDevice", self._mock_AVCaptureDevice)

        # Mock UIImagePickerController
        self._mock_UIImagePickerController = Mock()

        # On x86, the simulator crashes if you try to set the sourceType
        # for the picker, because the simulator doesn't support that source type.
        # On ARM, the hardware will let you show the dialog, but logs multiple errors.
        # Avoid the problem by using a neutral UIViewController. This also allows
        # us to mock behaviors that we can't do programmatically, like changing
        # the camera while the view is displayed.
        self._mock_picker = UIViewController.new()
        self._mock_UIImagePickerController.new.return_value = self._mock_picker

        # Simulate both cameras being available
        self._mock_UIImagePickerController.isCameraDeviceAvailable.return_value = True

        # Ensure the controller says that the camera source type is available.
        self._mock_UIImagePickerController.isSourceTypeAvailable.return_value = True

        # Flash is available on the rear camera
        def _mock_flash_available(device):
            return device == UIImagePickerControllerCameraDevice.Rear

        self._mock_UIImagePickerController.isFlashAvailableForCameraDevice = (
            _mock_flash_available
        )

        monkeypatch.setattr(
            iOS, "UIImagePickerController", self._mock_UIImagePickerController
        )

    def cleanup(self):
        try:
            picker = self.app.camera._impl.native
            result = picker.delegate.result
            if not result.future.done():
                picker.delegate.imagePickerControllerDidCancel(picker)
        except AttributeError:
            pass

    def known_cameras(self):
        return {
            "Rear": ("Rear", True),
            "Front": ("Front", False),
        }

    def select_other_camera(self):
        other = self.app.camera.devices[1]
        self.app.camera._impl.native.cameraDevice = other._impl.native
        return other

    def disconnect_cameras(self):
        # Set the source type as *not* available and re-create the Camera impl.
        self._mock_UIImagePickerController.isSourceTypeAvailable.return_value = False
        self.app.camera._impl = Camera(self.app)

    def reset_permission(self):
        self._mock_permissions = {}

    def grant_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = -1

    def allow_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = 1

    def reject_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = 0

    async def wait_for_camera(self, device_count=0):
        await self.redraw("Camera view displayed", delay=0.5)

    @property
    def shutter_enabled(self):
        # Shutter can't be disabled
        return True

    async def press_shutter_button(self, photo):
        # The camera picker was correctly configured
        picker = self.app.camera._impl.native
        assert picker.sourceType == UIImagePickerControllerSourceTypeCamera
        assert (
            picker.cameraCaptureMode == UIImagePickerControllerCameraCaptureMode.Photo
        )

        # Fake the result of a successful photo being taken
        image = toga.Image("resources/photo.png")
        picker.delegate.imagePickerController(
            picker,
            didFinishPickingMediaWithInfo={
                "UIImagePickerControllerOriginalImage": image._impl.native
            },
        )

        await self.redraw("Photo taken", delay=0.5)

        return await photo, picker.cameraDevice, picker.cameraFlashMode

    async def cancel_photo(self, photo):
        # The camera picker was correctly configured
        picker = self.app.camera._impl.native
        assert picker.sourceType == UIImagePickerControllerSourceTypeCamera
        assert (
            picker.cameraCaptureMode == UIImagePickerControllerCameraCaptureMode.Photo
        )

        # Fake the result of a cancelling the photo
        picker.delegate.imagePickerControllerDidCancel(picker)

        await self.redraw("Photo cancelled", delay=0.5)

        return await photo

    def same_device(self, device, native):
        if device is None:
            return native == UIImagePickerControllerCameraDevice.Rear
        else:
            return device._impl.native == native

    def same_flash_mode(self, expected, actual):
        return (
            expected
            == {
                UIImagePickerControllerCameraFlashMode.Auto: FlashMode.AUTO,
                UIImagePickerControllerCameraFlashMode.On: FlashMode.ON,
                UIImagePickerControllerCameraFlashMode.Off: FlashMode.OFF,
            }[actual]
        )
