from rubicon.objc import Block, objc_method

import toga
from toga.constants import FlashMode
from toga_iOS.libs import (
    AVAuthorizationStatus,
    AVCaptureDevice,
    AVMediaTypeVideo,
    UIImagePickerController,
    UIImagePickerControllerCameraCaptureMode,
    UIImagePickerControllerCameraDevice,
    UIImagePickerControllerCameraFlashMode,
    UIImagePickerControllerSourceTypeCamera,
)


class Device:
    def __init__(self, id, name, native):
        self._id = id
        self._name = name
        self.native = native

    def id(self):
        return self._id

    def name(self):
        return self._name

    def has_flash(self):
        return UIImagePickerController.isFlashAvailableForCameraDevice(self.native)


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


class TogaImagePickerController(UIImagePickerController):
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

        self.native = TogaImagePickerController.alloc().init()
        self.native.sourceType = UIImagePickerControllerSourceTypeCamera
        self.native.delegate = self.native

    def _has_permission(self, media_types, allow_unknown=False):
        if allow_unknown:
            valid_values = {
                AVAuthorizationStatus.Authorized.value,
                AVAuthorizationStatus.NotDetermined.value,
            }
        else:
            valid_values = {AVAuthorizationStatus.Authorized.value}

        return all(
            AVCaptureDevice.authorizationStatusForMediaType(media_type) in valid_values
            for media_type in media_types
        )

    def has_photo_permission(self, allow_unknown=False):
        return self._has_permission(
            [AVMediaTypeVideo],
            allow_unknown=allow_unknown,
        )

    # def has_video_permission(self, allow_unknown=False):
    #     return self._has_permission(
    #         [AVMediaTypeAudio, AVMediaTypeVideo],
    #         allow_unknown=allow_unknown,
    #     )

    def request_photo_permission(self, future):
        # This block is invoked when the permission is granted; however, permission is
        # granted from a different (inaccessible) thread, so it isn't picked up by
        # coverage.
        def permission_complete(result) -> None:  # pragma: no cover
            future.set_result(result)

        AVCaptureDevice.requestAccessForMediaType(
            AVMediaTypeVideo, completionHandler=Block(permission_complete, None, bool)
        )

    def get_devices(self):
        return (
            [
                Device(
                    id="Rear",
                    name="Rear",
                    native=UIImagePickerControllerCameraDevice.Rear,
                )
            ]
            if UIImagePickerController.isCameraDeviceAvailable(
                UIImagePickerControllerCameraDevice.Rear
            )
            else []
        ) + (
            [
                Device(
                    id="Front",
                    name="Front",
                    native=UIImagePickerControllerCameraDevice.Front,
                )
            ]
            if UIImagePickerController.isCameraDeviceAvailable(
                UIImagePickerControllerCameraDevice.Front
            )
            else []
        )

    def take_photo(self, result, device, flash):
        if self.has_photo_permission(allow_unknown=True):
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

            # Attach the result to the picker
            self.native.result = result

            # Show the pane
            toga.App.app.current_window._impl.native.rootViewController.presentViewController(
                self.native, animated=True, completion=None
            )
        else:
            raise PermissionError("App does not have permission to take photos")

    # def record_video(self, result, device, flash):
    #     if self.has_video_permission(allow_unknown=True):
    #         # Configure the controller to take a photo
    #         self.native.cameraCaptureMode = (
    #             UIImagePickerControllerCameraCaptureMode.Video
    #         )

    #         self.native.showsCameraControls = True
    #         self.native.cameraDevice = (
    #             device._impl.native
    #             if device
    #             else UIImagePickerControllerCameraDevice.Rear
    #         )
    #         self.native.cameraFlashMode = native_flash_mode(flash)

    #         # Attach the result to the picker
    #         self.native.result = result

    #         # Show the pane
    #         toga.App.app.current_window._impl.native.rootViewController.presentViewController(
    #             self.native, animated=True, completion=None
    #         )
    #     else:
    #         raise PermissionError("App does not have permission to take photos")
