from __future__ import annotations

import warnings
from threading import Thread

from rubicon.objc import Block, objc_method

import toga
from toga.colors import BLACK, RED
from toga.constants import FlashMode
from toga.style import Pack
from toga.style.pack import COLUMN

# for classes that need to be monkeypatched for testing
from toga_cocoa import libs as cocoa
from toga_cocoa.images import nsdata_to_bytes
from toga_cocoa.libs import (
    AVAuthorizationStatus,
    AVCaptureFlashMode,
    AVCapturePhotoOutput,
    AVCaptureSession,
    AVCaptureSessionPresetPhoto,
    AVCaptureVideoPreviewLayer,
    AVLayerVideoGravityResizeAspectFill,
    AVMediaTypeVideo,
    NSBundle,
)


def native_flash_mode(flash):
    return {
        FlashMode.ON: AVCaptureFlashMode.On,
        FlashMode.OFF: AVCaptureFlashMode.Off,
    }.get(flash, AVCaptureFlashMode.Auto)


class CameraDevice:
    def __init__(self, native):
        self.native = native

    def id(self):
        return str(self.native.uniqueID)

    def name(self):
        return str(self.native.localizedName)

    def has_flash(self):
        return self.native.isFlashAvailable()


# This is the native delegate, but we can't force the delegate to be invoked because we
# can't create a mock Photo; so we push all logic to the window, and mark this class no
# cover
class TogaCameraCaptureSession(AVCaptureSession):  # pragma: no cover
    @objc_method
    def captureOutput_didFinishProcessingPhoto_error_(
        self, output, photo, error
    ) -> None:
        # A photo has been taken.
        self.window.photo_taken(photo)


class TogaCameraWindow(toga.Window):
    def __init__(self, camera, device, flash, result):
        super().__init__(
            title="Camera",
            on_close=self.close_window,
            resizable=False,
            # This size is too small by design; it will be expanded by the layout rules.
            size=(640, 360),
        )
        self.camera = camera
        self.result = result

        self.create_preview_window()
        self.create_camera_session(device, flash)

    def create_preview_window(self):
        # A preview window, fixed 16:9 aspect ratio
        self.preview = toga.Box(style=Pack(width=640, height=360))

        # Set an initially empty list of devices. This will be populated once the window
        # is shown, so that getting the list of devices doesn't slow down showing the
        # capture window.
        self.device_select = toga.Selection(
            items=[],
            on_change=self.change_camera,
            style=Pack(width=200),
        )

        # The shutter button. Initially disabled until we know we have a camera available
        self.shutter_button = toga.Button(
            icon=toga.Icon("camera", system=True),
            on_press=self.take_photo,
            style=Pack(background_color=RED),
            enabled=False,
        )

        # The flash mode. Initially disable the flash.
        self.flash_mode = toga.Selection(
            items=[],
            style=Pack(width=75),
        )

        # Construct the overall layout
        self.content = toga.Box(
            children=[
                # The preview box will have its layer replaced by the the video preview.
                # Put the preview box inside another box so that we have a surface that
                # can show a black background while the camera is initializing.
                toga.Box(
                    children=[self.preview],
                    style=Pack(background_color=BLACK),
                ),
                toga.Box(
                    # Put the controls in a ROW box; the shutter button is
                    # in the middle, non-flexible, so that it is centered.
                    children=[
                        toga.Box(
                            children=[self.device_select],
                            style=Pack(flex=1),
                        ),
                        self.shutter_button,
                        toga.Box(
                            children=[
                                toga.Box(style=Pack(flex=1)),
                                toga.Label("Flash:"),
                                self.flash_mode,
                            ],
                            style=Pack(flex=1),
                        ),
                    ],
                    style=Pack(padding=10),
                ),
            ],
            style=Pack(direction=COLUMN),
        )

    # This is the method that creates the native camera session. Mocking these methods
    # is extremely difficult (impossible?); plus we can't know what cameras the test
    # machine will have. So - we mock this entire method, and mark it no-cover.
    def create_camera_session(self, device, flash):  # pragma: no cover
        self.camera_session = TogaCameraCaptureSession.alloc().init()
        self.camera_session.window = self
        self.camera_session.beginConfiguration()

        # Create a preview layer, rendering into the preview box
        preview_layer = AVCaptureVideoPreviewLayer.layerWithSession(self.camera_session)
        preview_layer.setVideoGravity(AVLayerVideoGravityResizeAspectFill)
        preview_layer.frame = self.preview._impl.native.bounds
        self.preview._impl.native.setLayer(preview_layer)

        # Specify that we want photo output.
        output = AVCapturePhotoOutput.alloc().init()
        output.setHighResolutionCaptureEnabled(True)
        self.camera_session.addOutput(output)
        self.camera_session.setSessionPreset(AVCaptureSessionPresetPhoto)

        # Set a sentinel for the camera input; this won't be set until the user has
        # selected a camera (either explicitly or implicitly)
        self.camera_input = None

        # Apply the configuration
        self.camera_session.commitConfiguration()

        # Polling camera devices and starting the camera session is a blocking activity.
        # Start a background thread to populate the list of camera devices and start the
        # camera session.
        Thread(
            target=self._enable_camera,
            kwargs={"device": device, "flash": flash},
        ).start()

    def _enable_camera(self, device, flash):
        self.camera_session.startRunning()

        # The GUI can only be modified from inside the GUI thread. Add a background task
        # to apply the new device list.
        self.camera.interface.app.loop.create_task(
            self._update_camera_list(toga.App.app.camera.devices, device, flash)
        )

    async def _update_camera_list(self, devices, device, flash):
        self.device_select.items = devices
        if device:
            self.device_select.value = device

        self._update_flash_mode(flash)

    def _update_flash_mode(self, flash=FlashMode.AUTO):
        if device := self.device_select.value:
            if device.has_flash:
                self.flash_mode.items = [FlashMode.AUTO, FlashMode.OFF, FlashMode.ON]
                self.flash_mode.value = flash
            else:
                self.flash_mode.items = [FlashMode.OFF]
        else:
            self.flash_mode.items = []

    def change_camera(self, widget=None, **kwargs):
        # Remove the existing camera input (if it exists)
        for input in self.camera_session.inputs:
            self.camera_session.removeInput(input)

        if device := self.device_select.value:
            input = cocoa.AVCaptureDeviceInput.deviceInputWithDevice(
                device._impl.native, error=None
            )
            self.camera_session.addInput(input)
            self.shutter_button.enabled = True
        else:
            self.shutter_button.enabled = False

        self._update_flash_mode()

    def close_window(self, widget, **kwargs):
        # If the user actually takes a photo, the window will be programmatically closed.
        # This handler is only triggered if the user manually closes the window.
        # Stop the camera session
        self.camera_session.stopRunning()

        # Set the "no result" result
        self.result.set_result(None)

        # Clear the reference to the preview window, and allow the window to close
        self.camera.preview_windows.remove(self)
        return True

    def take_photo(self, widget, **kwargs):
        settings = cocoa.AVCapturePhotoSettings.photoSettings()
        settings.flashMode = native_flash_mode(self.flash_mode.value)

        self.camera_session.outputs[0].capturePhotoWithSettings(
            settings,
            delegate=self.camera_session,
        )
        self.close()

    def photo_taken(self, photo):
        # Create the result image.
        image = toga.Image(nsdata_to_bytes(photo.fileDataRepresentation()))
        self.result.set_result(image)

        # Stop the camera session
        self.camera_session.stopRunning()

        # Clear the reference to the preview window.
        self.camera.preview_windows.remove(self)


class Camera:
    def __init__(self, interface):
        self.interface = interface

        if not NSBundle.mainBundle.objectForInfoDictionaryKey(
            "NSCameraUsageDescription"
        ):  # pragma: no cover
            # The app doesn't have the NSCameraUsageDescription key (e.g., via
            # `permission.camera` in Briefcase). No-cover because we can't manufacture
            # this condition in testing.
            msg = (
                "Application metadata does not declare that the app will use "
                "the camera. See "
                "https://toga.readthedocs.io/en/stable/reference/api/hardware/camera.html"
            )
            if self.interface.app.is_bundled:
                raise RuntimeError(msg)
            else:
                warnings.warn(msg)

        self.preview_windows = []

    def has_permission(self, allow_unknown=False):
        # To reset permissions to "factory" status, run:
        #     tccutil reset Camera
        #
        # To reset a single app:
        #     tccutil reset Camera <bundleID>
        #
        # e.g.
        #     tccutil reset Camera org.beeware.appname  # for a bundled app
        #     tccutil reset Camera com.microsoft.VSCode  # for code running in Visual Studio
        #     tccutil reset Camera com.apple.Terminal  # for code running in the Apple terminal

        if allow_unknown:
            valid_values = {
                AVAuthorizationStatus.Authorized.value,
                AVAuthorizationStatus.NotDetermined.value,
            }
        else:
            valid_values = {AVAuthorizationStatus.Authorized.value}

        return (
            cocoa.AVCaptureDevice.authorizationStatusForMediaType(AVMediaTypeVideo)
            in valid_values
        )

    def request_permission(self, future):
        # This block is invoked when the permission is granted; however, permission is
        # granted from a different (inaccessible) thread, so it isn't picked up by
        # coverage.
        def permission_complete(result) -> None:  # pragma: no cover
            future.set_result(result)

        cocoa.AVCaptureDevice.requestAccessForMediaType(
            AVMediaTypeVideo,
            completionHandler=Block(permission_complete, None, bool),
        )

    def get_devices(self):
        return [
            CameraDevice(device)
            for device in cocoa.AVCaptureDevice.devicesWithMediaType(AVMediaTypeVideo)
        ]

    def take_photo(self, result, device, flash):
        if self.has_permission(allow_unknown=True):
            window = TogaCameraWindow(self, device, flash, result)
            self.preview_windows.append(window)
            window.show()
        else:
            raise PermissionError("App does not have permission to take photos")
