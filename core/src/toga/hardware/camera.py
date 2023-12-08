from __future__ import annotations

from typing import Any, Protocol, TypeVar

import toga
from toga.constants import FlashMode
from toga.handlers import AsyncResult, wrapped_handler
from toga.platform import get_platform_factory


class PhotoResult(AsyncResult):
    RESULT_TYPE = "photo"


class PermissionResult(AsyncResult):
    RESULT_TYPE = "permission"


# class VideoResult(AsyncResult):
#     RESULT_TYPE = "video"


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

    @property
    def has_photo_permission(self) -> bool:
        """Does the user have permission to use camera devices?

        If the platform requires the user to explicitly confirm permission, and
        the user has not given confirmation, this will prompt the user to provide
        permission.
        """
        return self._impl.has_photo_permission()

    def request_photo_permission(
        self,
        on_result: CameraResultHandler[toga.Image] | None = None,
    ) -> PermissionResult:
        """Request sufficient permissions to capture photos.

        If permission has already been granted, this will return immediately
        without prompting the user.

        :param on_result: A handler that will be invoked with the success or
            failure of the request.
        :returns: An awaitable PermissionResult object. The PermissionResult
            object returns the success or failure of the permission request.
        """
        result = PermissionResult(wrapped_handler(self, on_result))

        if has_permission := self.has_photo_permission:
            result.set_result(has_permission)
            return result
        else:
            return self._impl.request_photo_permission(result)

    # def request_video_permission(
    #     self,
    #     on_result: CameraResultHandler[toga.Image] | None = None,
    # ) -> PermissionResult:
    #     result = PermissionResult(wrapped_handler(self, on_result))
    #
    #     if has_permission := self.has_video_permission:
    #         result.set_result(has_permission)
    #         return result
    #     else:
    #         return self._impl.request_video_permission(result)

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
        photo = PhotoResult(wrapped_handler(self, on_result))
        self._impl.take_photo(photo, device=device, flash=flash)
        return photo

    # def record_video(
    #     self,
    #     device: str | None = None,
    #     flash: FlashMode = FlashMode.AUTO,
    #     quality: VideoQuality = VideoQuality.MEDIUM,
    #     on_result: CamreaResultHandler[toga.Video] | None = None,
    # ) -> VideoResult:
    #     """Capture a video using one of the device's cameras.

    #     If the platform requires permission to access the camera and/or
    #     microphone, and the user hasn't previously provided that permission,
    #     this will cause permission to be requested.

    #     :param device: The camera device to use. If a specific device is *not*
    #         specified, a default camera will be used.
    #     :param flash: The flash mode to use; defaults to "auto"
    #     :param on_result: A callback that will be invoked when the photo has
    #         been taken (or the photo operation has been cancelled).
    #     :returns: An awaitable CameraResult object. The CameraResult object
    #         returns ``None`` when the user cancels the photo capture.
    #     """
    #     video = VideoResult()
    #     self._impl.record_video(
    #         video,
    #         device=device,
    #         flash=flash,
    #         on_result=wrapped_handler(self, on_result),
    #     )
    #     return video
