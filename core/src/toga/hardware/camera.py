from __future__ import annotations

from typing import Any, Protocol, TypeVar

import toga
from toga.constants import FlashMode
from toga.handlers import AsyncResult, wrapped_handler
from toga.platform import get_platform_factory


class PhotoResult(AsyncResult):
    RESULT_TYPE = "photo"

    def __init__(self):
        super().__init__()


# class VideoResult(AsyncResult):
#     RESULT_TYPE = "video"

#     def __init__(self):
#         super().__init__()


T = TypeVar("T")


class CameraResultHandler(Protocol[T]):
    def __call__(self, camera: Camera, result: T, **kwargs: Any) -> None:
        """A handler to invoke when a camera returns an image or video.

        :param camera: The camera
        :param result: The content returned by the camera.
        :param kwargs: Ensures compatibility with additional arguments introduced in
            future versions.
        """
        ...


class Camera:
    FRONT = "Front"
    REAR = "Rear"

    def __init__(self, app):
        self.factory = get_platform_factory()
        self._impl = self.factory.Camera(self)

    # @property
    # def has_permission(self) -> bool:
    #     """Does the user have permission to use camera devices?

    #     If the platform requires the user to explicitly confirm permission, and
    #     the user has not given confirmation, this will prompt the user to provide
    #     permission.
    #     """
    #     return self._impl.has_permission()

    @property
    def devices(self) -> list[str]:
        """The list of identifiers for available camera devices."""
        return self._impl.get_devices()

    def has_flash(self, device: str | None = None):
        """Does the camera device have a flash?

        :param device: The camera device to check. If a specific device is *not*
            specified, a default camera will be used.
        """
        return self.native.has_flash(device)

    def take_photo(
        self,
        device: str | None = None,
        flash: FlashMode = FlashMode.AUTO,
        on_result: CameraResultHandler[toga.Image] | None = None,
    ) -> PhotoResult:
        """Capture a photo using one of the device's cameras.

        If the platform requires permission to access the camera, and the user
        hasn't previously provided that permission, this will cause permission
        to be requested.

        :param device: The camera device to use. If a specific device is *not*
            specified, a default camera will be used.
        :param flash: The flash mode to use; defaults to "auto"
        :param on_result: A callback that will be invoked when the photo has
            been taken (or the photo operation has been cancelled).
        :returns: An awaitable CameraResult object. The CameraResult object
            returns ``None`` when the user cancels the photo capture.
        """
        photo = PhotoResult()
        self._impl.take_photo(
            photo,
            device=device,
            flash=flash,
            on_result=wrapped_handler(self, on_result),
        )
        return photo

    # def record_video(
    #     self,
    #     device: str | None = None,
    #     flash: FlashMode = FlashMode.AUTO,
    #     quality: VideoQuality = VideoQuality.MEDIUM,
    #     on_result: CamreaResultHandler[toga.Video] | None = None,
    # ) -> VideoResult:
    #     video = VideoResult()
    #     self._impl.record_video(
    #         video,
    #         device=device,
    #         flash=flash,
    #         on_result=wrapped_handler(self, on_result),
    #     )
    #     return video
