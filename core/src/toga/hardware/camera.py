from __future__ import annotations

import asyncio

import toga
from toga.constants import FlashMode
from toga.handlers import AsyncResult
from toga.platform import get_platform_factory


class PermissionResult(AsyncResult):
    RESULT_TYPE = "permission"


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

    def request_photo_permission(self) -> PermissionResult:
        """Request sufficient permissions to capture photos.

        If permission has already been granted, this will return without prompting the
        user.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the process of requesting permissions, but will return
        *immediately*. The return value can be awaited in an asynchronous context, but
        cannot be compared directly.

        :returns: An asynchronous result; when awaited, returns True if the app has
            permission to take a photo; False otherwise.
        """
        result = PermissionResult(None)

        if has_permission := self.has_photo_permission:
            result.set_result(has_permission)
        else:
            self._impl.request_photo_permission(result)

        return result

    # async def request_video_permission(self) -> bool:
    #     result = PermissionResult(None)
    #
    #     if has_permission := self.has_video_permission:
    #         result.set_result(has_permission)
    #     else:
    #         self._impl.request_video_permission(result)
    #
    #     return result

    @property
    def devices(self) -> list[str]:
        """The list of identifiers for available camera devices."""
        return self._impl.get_devices()

    def has_flash(self, device: str | None = None):
        """Does the specified camera device have a flash?

        :param device: The camera device to check. If a specific device is *not*
            specified, the features of the default camera will be returned.
        """
        return self._impl.has_flash(device)

    async def take_photo(
        self,
        device: str | None = None,
        flash: FlashMode = FlashMode.AUTO,
    ) -> toga.Image:
        """Capture a photo using one of the device's cameras.

        If the platform requires permission to access the camera, and the user
        hasn't previously provided that permission, this will cause permission
        to be requested.

        :param device: The camera device to use. If a specific device is *not*
            specified, a default camera will be used.
        :param flash: The flash mode to use; defaults to "auto"
        :returns: The :any:`toga.Image` captured by the camera.
        """
        future = asyncio.get_event_loop().create_future()
        self._impl.take_photo(future, device=device, flash=flash)
        return await future

    # async def record_video(
    #     self,
    #     device: str | None = None,
    #     flash: FlashMode = FlashMode.AUTO,
    #     quality: VideoQuality = VideoQuality.MEDIUM,
    # ) -> toga.Video:
    #     """Capture a video using one of the device's cameras.
    #
    #     If the platform requires permission to access the camera and/or
    #     microphone, and the user hasn't previously provided that permission,
    #     this will cause permission to be requested.
    #
    #     :param device: The camera device to use. If a specific device is *not*
    #         specified, a default camera will be used.
    #     :param flash: The flash mode to use; defaults to "auto"
    #     :returns: The :any:`toga.Video` captured by the camera.
    #     """
    #     future = asyncio.get_event_loop().create_future()
    #     self._impl.record_video(future, device=device, flash=flash)
    #     return future
