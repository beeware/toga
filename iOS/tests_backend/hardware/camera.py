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
            try:
                self._mock_permissions[str(media_type)] = abs(
                    self._mock_permissions[str(media_type)]
                )
                result = bool(self._mock_permissions[str(media_type)])
            except KeyError:
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

        # Mock AVCaptureSession for scanning
        self._mock_session = Mock()
        self._mock_session.running.return_value = False
        self._mock_AVCaptureSession = Mock()
        self._mock_AVCaptureSession.new.return_value = None

        def _session_alloc_init():
            return self._mock_session

        self._mock_AVCaptureSession.alloc = Mock()
        self._mock_AVCaptureSession.alloc.init = _session_alloc_init
        monkeypatch.setattr(iOS, "AVCaptureSession", self._mock_AVCaptureSession)

        # Mock AVCaptureDeviceInput
        self._mock_AVCaptureDeviceInput = Mock()
        monkeypatch.setattr(
            iOS, "AVCaptureDeviceInput", self._mock_AVCaptureDeviceInput
        )

        # Mock AVCaptureMetadataOutput
        self._mock_metadata_output = Mock()
        self._mock_metadata_output.isKindOfClass_.return_value = True
        self._mock_AVCaptureMetadataOutput = Mock()
        self._mock_AVCaptureMetadataOutput.alloc = Mock()
        self._mock_AVCaptureMetadataOutput.alloc.init.return_value = (
            self._mock_metadata_output
        )
        monkeypatch.setattr(
            iOS, "AVCaptureMetadataOutput", self._mock_AVCaptureMetadataOutput
        )

        # Wire up session.outputs() to return the mocked metadata output
        self._mock_session.outputs.return_value = [self._mock_metadata_output]

        # Mock AVCaptureVideoPreviewLayer
        self._mock_preview_layer = Mock()
        self._mock_AVCaptureVideoPreviewLayer = Mock()
        self._mock_AVCaptureVideoPreviewLayer.layerWithSession.return_value = (
            self._mock_preview_layer
        )
        monkeypatch.setattr(
            iOS, "AVCaptureVideoPreviewLayer", self._mock_AVCaptureVideoPreviewLayer
        )

        # Mock AVMetadataMachineReadableCodeObject
        self._mock_code_object = Mock()
        monkeypatch.setattr(
            iOS,
            "AVMetadataMachineReadableCodeObject",
            self._mock_code_object,
        )

        # Mock the metadata object type constants
        for const_name in [
            "AVMetadataObjectTypeQRCode",
            "AVMetadataObjectTypeCode128Code",
            "AVMetadataObjectTypeEAN13Code",
            "AVMetadataObjectTypeEAN8Code",
            "AVMetadataObjectTypePDF417Code",
            "AVMetadataObjectTypeAztecCode",
            "AVMetadataObjectTypeDataMatrixCode",
        ]:
            monkeypatch.setattr(iOS, const_name, f"AVMetadataObjectType{const_name}")

        # Mock devicesWithMediaType to return a mock rear camera device
        self._mock_rear_device = Mock()
        self._mock_rear_device.position.return_value = 1  # back
        self._mock_AVCaptureDevice.devicesWithMediaType.return_value = [
            self._mock_rear_device
        ]

        # Mock deviceInputWithDevice_error_
        self._mock_input = Mock()
        self._mock_AVCaptureDeviceInput.deviceInputWithDevice_error_.return_value = (
            self._mock_input
        )

        # Load an image that can be used as a sample photo
        self.camera_image = toga.Image("resources/photo.png")

    def cleanup(self):
        try:
            picker = self.app.camera._impl.native
            result = picker.delegate.result
            if not result.future.done():
                picker.delegate.imagePickerControllerDidCancel(picker)
        except AttributeError:
            pass
        # Clean up any active scanner
        try:
            if self.app.camera._impl.is_scanning():
                self.app.camera._impl.stop_scanning()
        except (NotImplementedError, AttributeError):
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
        self._mock_UIImagePickerController.isSourceTypeAvailable.return_value = False
        self.app.camera._impl = Camera(self.app)

    def reset_permission(self):
        self._mock_permissions = {}

    def grant_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = 1

    def allow_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = -1

    def reject_permission(self):
        self._mock_permissions[str(AVMediaTypeVideo)] = 0

    async def wait_for_camera(self, device_count=0):
        await self.redraw("Camera view displayed", delay=0.5)

    @property
    def shutter_enabled(self):
        return True

    async def press_shutter_button(self, photo):
        picker = self.app.camera._impl.native
        assert picker.sourceType == UIImagePickerControllerSourceTypeCamera
        assert (
            picker.cameraCaptureMode == UIImagePickerControllerCameraCaptureMode.Photo
        )

        picker.delegate.imagePickerController(
            picker,
            didFinishPickingMediaWithInfo={
                "UIImagePickerControllerOriginalImage": self.camera_image._impl.native
            },
        )

        await self.redraw("Photo taken", delay=0.5)

        return await photo, picker.cameraDevice, picker.cameraFlashMode

    async def cancel_photo(self, photo):
        picker = self.app.camera._impl.native
        assert picker.sourceType == UIImagePickerControllerSourceTypeCamera
        assert (
            picker.cameraCaptureMode == UIImagePickerControllerCameraCaptureMode.Photo
        )

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

    async def simulate_scan_detection(self, content="scanned_content"):
        """Simulate a barcode being detected during scanning."""
        impl = self.app.camera._impl
        impl._handle_detection(content)
        await self.redraw("Scan detected", delay=0.1)

    async def cancel_scan(self):
        """Simulate the user cancelling scanning."""
        impl = self.app.camera._impl
        impl.stop_scanning()
        await self.redraw("Scan cancelled", delay=0.1)

    async def wait_for_scan_start(self):
        """Wait for the scanner to be initialized."""
        await self.redraw("Scanner started", delay=0.3)
