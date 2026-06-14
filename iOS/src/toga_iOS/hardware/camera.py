import warnings
from functools import cache

from rubicon.objc import SEL, Block, NSObject, ObjCClass, objc_const, objc_method

import toga
from toga.constants import BarcodeFormat, FlashMode
from toga_iOS import libs as iOS
from toga_iOS.libs import (
    AVAuthorizationStatus,
    AVMediaTypeVideo,
    NSBundle,
    UIButton,
    UIColor,
    UIControlEventTouchUpInside,
    UIControlStateNormal,
    UIImagePickerControllerCameraCaptureMode,
    UIImagePickerControllerCameraDevice,
    UIImagePickerControllerCameraFlashMode,
    UIImagePickerControllerSourceTypeCamera,
    UIViewController,
)

AVCaptureDevicePositionBack = 1
AVCaptureDevicePositionFront = 2


class CameraDevice:
    def __init__(self, id, name, native):
        self._id = id
        self._name = name
        self.native = native

    def id(self):
        return self._id

    def name(self):
        return self._name

    def has_flash(self):
        return iOS.UIImagePickerController.isFlashAvailableForCameraDevice(self.native)


def native_flash_mode(flash):
    return {
        FlashMode.ON: UIImagePickerControllerCameraFlashMode.On,
        FlashMode.OFF: UIImagePickerControllerCameraFlashMode.Off,
    }.get(flash, UIImagePickerControllerCameraFlashMode.Auto)


@cache
def _scan_symbols():
    av_foundation = iOS.av_foundation
    return {
        "capture_device": ObjCClass("AVCaptureDevice"),
        "capture_device_input": ObjCClass("AVCaptureDeviceInput"),
        "capture_metadata_output": ObjCClass("AVCaptureMetadataOutput"),
        "capture_session": ObjCClass("AVCaptureSession"),
        "capture_video_preview_layer": ObjCClass("AVCaptureVideoPreviewLayer"),
        "metadata_machine_readable_code_object": ObjCClass(
            "AVMetadataMachineReadableCodeObject"
        ),
        "video_gravity_resize_aspect_fill": objc_const(
            av_foundation, "AVLayerVideoGravityResizeAspectFill"
        ),
        "barcode_format_map": {
            BarcodeFormat.QR: objc_const(av_foundation, "AVMetadataObjectTypeQRCode"),
            BarcodeFormat.CODE128: objc_const(
                av_foundation, "AVMetadataObjectTypeCode128Code"
            ),
            BarcodeFormat.EAN13: objc_const(
                av_foundation, "AVMetadataObjectTypeEAN13Code"
            ),
            BarcodeFormat.EAN8: objc_const(
                av_foundation, "AVMetadataObjectTypeEAN8Code"
            ),
            BarcodeFormat.PDF417: objc_const(
                av_foundation, "AVMetadataObjectTypePDF417Code"
            ),
            BarcodeFormat.AZTEC: objc_const(
                av_foundation, "AVMetadataObjectTypeAztecCode"
            ),
            BarcodeFormat.DATA_MATRIX: objc_const(
                av_foundation, "AVMetadataObjectTypeDataMatrixCode"
            ),
        },
    }


class TogaImagePickerDelegate(NSObject):
    @objc_method
    def imagePickerController_didFinishPickingMediaWithInfo_(
        self, picker, info
    ) -> None:
        picker.dismissViewControllerAnimated(True, completion=None)

        image = toga.Image(info["UIImagePickerControllerOriginalImage"])
        self.result.set_result(image)

    @objc_method
    def imagePickerControllerDidCancel_(self, picker) -> None:
        picker.dismissViewControllerAnimated(True, completion=None)
        self.result.set_result(None)


class TogaCameraScannerDelegate(NSObject):
    @objc_method
    def metadataOutput_didOutputMetadataObjects_fromConnection_(
        self, output, metadata_objects, connection
    ) -> None:
        count = metadata_objects.count()
        if count > 0:
            metadata_object = metadata_objects.objectAtIndex(0)
            if metadata_object.isKindOfClass_(
                _scan_symbols()["metadata_machine_readable_code_object"]
            ):
                content = str(metadata_object.stringValue())
                if content:
                    self.camera._handle_detection(content)

    @objc_method
    def cancelScanning_(self, sender) -> None:
        self.camera.stop_scanning()


class Camera:
    def __init__(self, interface):
        self.interface = interface

        if NSBundle.mainBundle.objectForInfoDictionaryKey("NSCameraUsageDescription"):
            self._scan_session = None
            self._scan_preview_controller = None
            self._scan_delegate = None
            self._scan_future = None
            self._scan_continuous = False

            if iOS.UIImagePickerController.isSourceTypeAvailable(
                UIImagePickerControllerSourceTypeCamera
            ):
                self.native = iOS.UIImagePickerController.new()
                self.native.sourceType = UIImagePickerControllerSourceTypeCamera
                self.delegate_link = TogaImagePickerDelegate.new()
                self.native.delegate = self.delegate_link
            else:
                self.native = None
        else:  # pragma: no cover
            raise RuntimeError(
                "Application metadata does not declare that the "
                "app will use the camera."
            )

    def has_permission(self, allow_unknown=False):
        if allow_unknown:
            valid_values = {
                AVAuthorizationStatus.Authorized.value,
                AVAuthorizationStatus.NotDetermined.value,
            }
        else:
            valid_values = {AVAuthorizationStatus.Authorized.value}

        return (
            iOS.AVCaptureDevice.authorizationStatusForMediaType(AVMediaTypeVideo)
            in valid_values
        )

    def request_permission(self, future):
        def permission_complete(result) -> None:
            future.set_result(result)

        iOS.AVCaptureDevice.requestAccessForMediaType(
            AVMediaTypeVideo, completionHandler=Block(permission_complete, None, bool)
        )

    def get_devices(self):
        return (
            [
                CameraDevice(
                    id="Rear",
                    name="Rear",
                    native=UIImagePickerControllerCameraDevice.Rear,
                )
            ]
            if iOS.UIImagePickerController.isCameraDeviceAvailable(
                UIImagePickerControllerCameraDevice.Rear
            )
            else []
        ) + (
            [
                CameraDevice(
                    id="Front",
                    name="Front",
                    native=UIImagePickerControllerCameraDevice.Front,
                )
            ]
            if iOS.UIImagePickerController.isCameraDeviceAvailable(
                UIImagePickerControllerCameraDevice.Front
            )
            else []
        )

    def take_photo(self, result, device, flash):
        if self.native is None:
            warnings.warn("No camera is available", stacklevel=2)
            result.set_result(None)
        elif self.has_permission(allow_unknown=True):
            self.native.cameraCaptureMode = (
                UIImagePickerControllerCameraCaptureMode.Photo
            )

            self.native.showsCameraControls = True
            self.native.cameraDevice = (
                device._impl.native
                if device
                else UIImagePickerControllerCameraDevice.Rear
            )
            self.native.cameraFlashMode = native_flash_mode(flash)

            self.native.delegate.result = result

            (
                toga.App.app.current_window._impl.native.rootViewController
            ).presentViewController(self.native, animated=True, completion=None)
        else:
            raise PermissionError("App does not have permission to take photos")

    def is_scanning(self):
        return self._scan_session is not None

    def start_scanning(self, future, device, code_types, continuous):
        if not self.has_permission(allow_unknown=True):
            raise PermissionError("App does not have permission to take photos")

        self._scan_future = future
        self._scan_continuous = continuous

        session = self._build_scan_session(device, code_types)
        if session is None:
            future.set_result(None)
            return

        self._scan_delegate = TogaCameraScannerDelegate.alloc().init()
        self._scan_delegate.camera = self

        capture_metadata_output = _scan_symbols()["capture_metadata_output"]
        for output in session.outputs():
            if output.isKindOfClass_(capture_metadata_output):
                output.setMetadataObjectsDelegate_queue_(self._scan_delegate, None)
                break

        self._scan_preview_controller = self._build_scan_ui(session)
        self._scan_session = session

        session.startRunning()
        self._present_scan_ui(self._scan_preview_controller)

    def _build_scan_session(self, device, code_types):
        symbols = _scan_symbols()
        session = symbols["capture_session"].alloc().init()

        capture_device = self._resolve_capture_device(device)
        if capture_device is None:
            warnings.warn("No camera is available for scanning", stacklevel=2)
            return None

        device_input = symbols["capture_device_input"].deviceInputWithDevice_error_(
            capture_device, None
        )
        if not session.canAddInput(device_input):
            warnings.warn("Cannot add camera input", stacklevel=2)
            return None
        session.addInput(device_input)

        metadata_output = symbols["capture_metadata_output"].alloc().init()
        if not session.canAddOutput(metadata_output):
            warnings.warn("Cannot add metadata output", stacklevel=2)
            return None
        session.addOutput(metadata_output)

        objc_types = [
            symbols["barcode_format_map"][ct]
            for ct in code_types
            if ct in symbols["barcode_format_map"]
        ]
        if objc_types:
            metadata_output.setMetadataObjectTypes_(objc_types)

        return session

    def _resolve_capture_device(self, device):
        position = (
            AVCaptureDevicePositionFront
            if device is not None
            and device._impl.native == UIImagePickerControllerCameraDevice.Front
            else AVCaptureDevicePositionBack
        )
        for dev in _scan_symbols()["capture_device"].devicesWithMediaType(
            AVMediaTypeVideo
        ):
            if dev.position() == position:
                return dev
        return None

    def _build_scan_ui(self, session):
        symbols = _scan_symbols()
        preview_layer = symbols["capture_video_preview_layer"].layerWithSession(session)
        preview_layer.setVideoGravity(symbols["video_gravity_resize_aspect_fill"])

        controller = UIViewController.alloc().init()
        controller.view.layer().insertSublayer_atIndex_(preview_layer, 0)

        cancel_button = UIButton.buttonWithType_(0)
        cancel_button.setTitle_forState_("Cancel", UIControlStateNormal)
        cancel_button.setTitleColor_forState_(
            UIColor.whiteColor(), UIControlStateNormal
        )
        cancel_button.sizeToFit()
        cancel_button.addTarget_action_forControlEvents_(
            self._scan_delegate, SEL("cancelScanning:"), UIControlEventTouchUpInside
        )
        cancel_button.setTranslatesAutoresizingMaskIntoConstraints(True)
        controller.view.addSubview(cancel_button)

        preview_layer.frame = controller.view.bounds
        return controller

    def _present_scan_ui(self, controller):
        (
            toga.App.app.current_window._impl.native.rootViewController
        ).presentViewController(controller, animated=True, completion=None)

    def stop_scanning(self):
        if self._scan_session is not None:
            self._scan_session.stopRunning()
            self._scan_session = None

        if self._scan_preview_controller is not None:
            self._scan_preview_controller.dismissViewControllerAnimated(
                True, completion=None
            )
            self._scan_preview_controller = None

        if self._scan_future is not None:
            self._scan_future.set_result(None)
            self._scan_future = None

        self._scan_delegate = None
        self._scan_continuous = False

    def _handle_detection(self, content):
        self.interface.on_detection(content=content)
        if not self._scan_continuous:
            self.stop_scanning()
