from __future__ import annotations

import abc
from collections.abc import Iterable
from typing import TYPE_CHECKING, Protocol

from toga.constants import FlashMode
from toga.handlers import AsyncResult, PermissionResult
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App
    from toga.widgets.base import Widget


class PhotoResult(AsyncResult):
    RESULT_TYPE = "photo"


class PlatformCameraDevice(abc.ABC):
    """Interface required for a platform's camera devices."""

    @abc.abstractmethod
    def id(self) -> str:
        """Get the unique identifier for the device."""
        ...

    @abc.abstractmethod
    def name(self) -> str:
        """Get a human-readable name for the device."""
        ...

    @abc.abstractmethod
    def has_flash(self) -> bool:
        """Whether the device has flash."""
        ...


class CameraDevice:
    def __init__(self, impl: PlatformCameraDevice):
        self._impl = impl

    @property
    def id(self) -> str:
        """A unique identifier for the device"""
        return self._impl.id()

    @property
    def name(self) -> str:
        """A human-readable name for the device"""
        return self._impl.name()

    @property
    def has_flash(self) -> bool:
        """Does the device have a flash?"""
        return self._impl.has_flash()

    def __eq__(self, other: Widget) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return f"<CameraDevice id={self.id} {self.name!r}>"

    def __str__(self) -> str:
        return self.name


class CameraInterface(Protocol):
    app: App
    """The currently running application."""


class PlatformCamera(abc.ABC):
    """Interface required of each platform's ``Camera`` implementation."""

    interface: CameraInterface
    """Application location interface, containing a change-handler reference."""

    def __init__(self, interface: CameraInterface):
        self.interface = interface

    @abc.abstractmethod
    def has_permission(self) -> bool:
        """Whether the application has permission to use the camera."""
        ...

    @abc.abstractmethod
    def request_permission(self, result: PermissionResult) -> None:
        """Asynchronously request permission to use the camera.

        :param result: a future representing the result of the permission request."""
        ...

    @abc.abstractmethod
    def get_devices(self) -> Iterable[PlatformCameraDevice]:
        """List the available cameras."""
        ...

    @abc.abstractmethod
    def take_photo(
        self, result, *, device: CameraDevice | None, flash: FlashMode
    ) -> None:
        """Asynchronously take a photo with the specified device and flash setting.

        If permissions have not been requested, permission should be requested before
        taking the photo.

        :param result: A future representing the path to the file of the photograph.
        :param device: A device with which to take the photo. If none is provided, the
            most appropriate default should be used.
        :param flash: The flash mode to use when taking the photograph.
        """
        ...


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
    def has_permission(self) -> bool:
        """Does the app have permission to use camera devices?

        If the platform requires the user to explicitly confirm permission, and
        the user has not yet given permission, this will return ``False``.
        """
        return self._impl.has_permission()

    def request_permission(self) -> PermissionResult:
        """Request sufficient permissions to capture photos.

        If permission has already been granted, this will return without prompting the
        user.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the process of requesting permissions, but will return
        *immediately*. The return value can be awaited in an asynchronous context, but
        cannot be used directly.

        :returns: An asynchronous result; when awaited, returns True if the app has
            permission to take a photo; False otherwise.
        """
        result = PermissionResult(None)

        if has_permission := self.has_permission:
            result.set_result(has_permission)
        else:
            self._impl.request_permission(result)

        return result

    @property
    def devices(self) -> list[CameraDevice]:
        """The list of available camera devices."""
        return [CameraDevice(impl) for impl in self._impl.get_devices()]

    def take_photo(
        self,
        device: CameraDevice | None = None,
        flash: FlashMode = FlashMode.AUTO,
    ) -> PhotoResult:
        """Capture a photo using one of the device's cameras.

        If the platform requires permission to access the camera, and the user hasn't
        previously provided that permission, this will cause permission to be requested.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the process of taking a photo, but will return
        *immediately*. The return value can be awaited in an asynchronous context, but
        cannot be used directly.

        :param device: The initial camera device to use. If a device is *not* specified,
            a default camera will be used. Depending on the hardware available, the user
            may be able to change the camera used to capture the image at runtime.
        :param flash: The initial flash mode to use; defaults to "auto". Depending on
            the hardware available, this may be modified by the user at runtime.
        :returns: An asynchronous result; when awaited, returns the :any:`toga.Image`
            captured by the camera, or ``None`` if the photo was  cancelled.
        :raises PermissionError: if the app does not have permission to use the camera.
        """
        photo = PhotoResult(None)
        self._impl.take_photo(photo, device=device, flash=flash)
        return photo
