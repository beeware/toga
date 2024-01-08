from __future__ import annotations

from typing import TYPE_CHECKING, Any

from toga.constants import FlashMode
from toga.handlers import AsyncResult
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App


class PermissionResult(AsyncResult):
    RESULT_TYPE = "permission"


class PhotoResult(AsyncResult):
    RESULT_TYPE = "photo"


class Device:
    def __init__(self, id: str, name: str, native: Any):
        self._id = id
        self._name = name
        self._native = native

    @property
    def id(self) -> str:
        """A unique identifier for the device"""
        return self._id

    @property
    def name(self) -> str:
        """A human-readable name for the device"""
        return self._name

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self._name


class Camera:
    def __init__(self, app: App):
        self.factory = get_platform_factory()
        self._app = app
        self._impl = self.factory.Camera(self)

    @property
    def app(self) -> App:
        """The app with which the camera is associated"""
        return self._app

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
    def devices(self) -> list[Device]:
        """The list of available camera devices."""
        return self._impl.get_devices()

    def has_flash(self, device: Device | None = None):
        """Does the specified camera device have a flash?

        :param device: The camera device to check. If a specific device is *not*
            specified, the features of the default camera will be returned.
        """
        return self._impl.has_flash(device)

    def take_photo(
        self,
        device: Device | None = None,
        flash: FlashMode = FlashMode.AUTO,
    ) -> PhotoResult:
        """Capture a photo using one of the device's cameras.

        If the platform requires permission to access the camera, and the user hasn't
        previously provided that permission, this will cause permission to be requested.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the process of requesting permissions, but will return
        *immediately*. The return value can be awaited in an asynchronous context, but
        cannot be compared directly.

        :param device: The camera device to use. If a specific device is *not*
            specified, a default camera will be used.
        :param flash: The flash mode to use; defaults to "auto"
        :returns: An asynchronous result; when awaited, returns the :any:`toga.Image`
            captured by the camera, or ``None`` if the photo was  cancelled.
        """
        photo = PhotoResult(None)
        self._impl.take_photo(photo, device=device, flash=flash)
        return photo

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
