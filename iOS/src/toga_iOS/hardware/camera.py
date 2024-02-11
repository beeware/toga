import warnings

from rubicon.objc import Block, NSObject, objc_method

import toga
from toga.constants import FlashMode

# for classes that need to be monkeypatched for testing
from toga_iOS import libs as iOS
from toga_iOS.libs import (
    AVAuthorizationStatus,
    AVMediaTypeVideo,
    NSBundle,
    UIImagePickerControllerCameraCaptureMode,
    UIImagePickerControllerCameraDevice,
    UIImagePickerControllerCameraFlashMode,
    UIImagePickerControllerSourceTypeCamera,
)


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


# def native_video_quality(quality):
#     return {
#         VideoQuality.HIGH: UIImagePickerControllerQualityType.High,
#         VideoQuality.LOW: UIImagePickerControllerQualityType.Low,
#     }.get(quality, UIImagePickerControllerQualityType.Medium)


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


class Camera:
    def __init__(self, interface):
        self.interface = interface

        if NSBundle.mainBundle.objectForInfoDictionaryKey("NSCameraUsageDescription"):
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
            # The app doesn't have the NSCameraUsageDescription key (e.g., via
            # `permission.camera` in Briefcase). No-cover because we can't manufacture
            # this condition in testing.
            raise RuntimeError(
                "Application metadata does not declare that the app will use the camera."
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
        # This block is invoked when the permission is granted; however, permission is
        # granted from a different (inaccessible) thread, so it isn't picked up by
        # coverage.
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
            warnings.warn("No camera is available")
            result.set_result(None)
        elif self.has_permission(allow_unknown=True):
            # Configure the controller to take a photo
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

            # Attach the result to the delegate
            self.native.delegate.result = result

            # Show the pane
            toga.App.app.current_window._impl.native.rootViewController.presentViewController(
                self.native, animated=True, completion=None
            )
        else:
            raise PermissionError("App does not have permission to take photos")
