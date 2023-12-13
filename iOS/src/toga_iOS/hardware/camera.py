from rubicon.objc import objc_method

import toga
from toga.constants import FlashMode, VideoQuality
from toga.hardware.camera import Camera as TogaCamera
from toga_iOS.libs import (
    AVAuthorizationStatus,
    AVCaptureDevice,
    AVMediaTypeVideo,
    UIImagePickerController,
    UIImagePickerControllerCameraCaptureMode,
    UIImagePickerControllerCameraDevice,
    UIImagePickerControllerCameraFlashMode,
    UIImagePickerControllerQualityType,
    UIImagePickerControllerSourceTypeCamera,
)


def native_device(device):
    try:
        return {
            # Rear camera is the default
            None: UIImagePickerControllerCameraDevice.Rear,
            TogaCamera.FRONT: UIImagePickerControllerCameraDevice.Front,
            TogaCamera.REAR: UIImagePickerControllerCameraDevice.Rear,
        }[device]
    except KeyError:
        return ValueError("Unknown camera device {device!r}")


def native_flash_mode(flash):
    return {
        FlashMode.ON: UIImagePickerControllerCameraFlashMode.On,
        FlashMode.OFF: UIImagePickerControllerCameraFlashMode.Off,
    }.get(flash, UIImagePickerControllerCameraFlashMode.Auto)


def native_video_quality(quality):
    return {
        VideoQuality.HIGH: UIImagePickerControllerQualityType.High,
        VideoQuality.LOW: UIImagePickerControllerQualityType.Low,
    }.get(quality, UIImagePickerControllerQualityType.Medium)


class TogaImagePickerController(UIImagePickerController):
    @objc_method
    def imagePickerController_didFinishPickingMediaWithInfo_(
        self, picker, info
    ) -> None:
        picker.dismissViewControllerAnimated(True, completion=None)

        image = toga.Image(info["UIImagePickerControllerOriginalImage"])
        self.future.set_result(image)

        picker.delegate.release()

    @objc_method
    def imagePickerControllerDidCancel_(self, picker) -> None:
        picker.dismissViewControllerAnimated(True, completion=None)

        self.future.set_result(None)

        picker.delegate.release()


class Camera:
    def __init__(self, interface):
        self.interface = interface

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
        def video_complete(permission: bool) -> None:
            future.set_result(permission)

        AVCaptureDevice.requestAccessForMediaType(
            AVMediaTypeVideo,
            completionHandler=video_complete,
        )

    def get_devices(self):
        return (
            [TogaCamera.REAR]
            if self.native.isCameraDeviceAvailable(
                UIImagePickerControllerCameraDevice.Rear
            )
            else []
        ) + (
            [TogaCamera.FRONT]
            if self.native.isCameraDeviceAvailable(
                UIImagePickerControllerCameraDevice.Front
            )
            else []
        )

    def has_flash(self, device):
        return self.native.isFlashAvailableForCameraDevice(native_device(device))

    def take_photo(self, future, device, flash):
        if self.has_photo_permission(allow_unknown=True):
            # Configure the controller to take a photo
            camera_session = TogaImagePickerController.alloc().init()
            camera_session.sourceType = UIImagePickerControllerSourceTypeCamera
            camera_session.cameraCaptureMode = (
                UIImagePickerControllerCameraCaptureMode.Photo
            )

            camera_session.showsCameraControls = True
            camera_session.cameraDevice = native_device(device)
            camera_session.cameraFlashMode = native_flash_mode(flash)

            # Create a delegate to handle the callback
            camera_session.future = future
            camera_session.delegate = camera_session

            # Show the pane
            toga.App.app.current_window._impl.native.rootViewController.presentViewController(
                camera_session, animated=True, completion=None
            )
        else:
            raise PermissionError("App does not have permission to take photos")

    # def record_video(self, future, device, flash):
    #     if self.has_video_permission(allow_unknown=True):
    #         # Configure the controller to take a photo
    #         camera_session = TogaImagePickerController.alloc().init()
    #         camera_session.sourceType = UIImagePickerControllerSourceTypeCamera
    #         camera_session.cameraCaptureMode = (
    #             UIImagePickerControllerCameraCaptureMode.Video
    #         )

    #         camera_session.showsCameraControls = True
    #         camera_session.cameraDevice = native_device(device)
    #         camera_session.cameraFlashMode = native_flash_mode(flash)

    #         # Create a delegate to handle the callback
    #         camera_session.future = future
    #         camera_session.delegate = camera_session

    #         # Show the pane
    #         toga.App.app.current_window._impl.native.rootViewController.presentViewController(
    #             camera_session, animated=True, completion=None
    #         )
    #     else:
    #         raise PermissionError("App does not have permission to take photos")
