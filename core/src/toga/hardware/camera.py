from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from toga.constants import BarcodeFormat, FlashMode
from toga.handlers import AsyncResult, PermissionResult, wrapped_handler
from toga.platform import get_factory

if TYPE_CHECKING:
    from toga.app import App
    from toga.widgets.base import Widget


class PhotoResult(AsyncResult):
    RESULT_TYPE = "photo"


class ScanResult(AsyncResult):
    RESULT_TYPE = "scan"


class CameraDevice:
    def __init__(self, impl: Any):
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


class Camera:
    def __init__(self, app: App):
        self.factory = get_factory()
        self._app = app
        self._impl = self.factory.Camera(self)
        self._on_detection = wrapped_handler(self, None)

    @property
    def app(self) -> App:
        """The app with which the camera is associated"""
        return self._app

    @property
    def has_permission(self) -> bool:
        """Does the user have permission to use camera devices?

        If the platform requires the user to explicitly confirm permission, and
        the user has not yet given permission, this will return `False`.
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
        :returns: An asynchronous result; when awaited, returns the [`toga.Image`][]
            captured by the camera, or `None` if the photo was  cancelled.
        :raises PermissionError: if the app does not have permission to use the camera.
        """
        photo = PhotoResult(None)
        self._impl.take_photo(photo, device=device, flash=flash)
        return photo

    @property
    def on_detection(self) -> Callable:
        """A handler to invoke when a barcode is detected during scanning.

        The callback receives the camera as the first argument, and the detected content
        as a keyword argument: ``on_detection(camera, content=content)``.

        If scanning was started with ``continuous=True``, the callback will be invoked
        each time a barcode is detected. If ``continuous=False`` (the default), the
        callback is invoked once before scanning stops automatically.
        """
        return self._on_detection

    @on_detection.setter
    def on_detection(self, handler: Callable | None) -> None:
        self._on_detection = wrapped_handler(self, handler)

    @property
    def is_scanning(self) -> bool:
        """Is the camera currently scanning for barcodes?"""
        return self._impl.is_scanning()

    def start_scanning(
        self,
        device: CameraDevice | None = None,
        code_types: list[BarcodeFormat] | None = None,
        on_detection: Callable | None = None,
        continuous: bool = False,
    ) -> ScanResult:
        """Start scanning for barcodes (including QR codes) in real-time.

        Displays a live camera preview that scans for supported barcode types. When a
        barcode is detected, the ``on_detection`` callback is invoked.

        If ``continuous`` is ``False`` (the default), scanning stops automatically after
        the first detection, and the returned ``ScanResult`` resolves with the detected
        content string. If ``continuous`` is ``True``, scanning continues until
        :meth:`stop_scanning` is called, and the ``ScanResult`` resolves with ``None``.

        If the platform requires permission to access the camera, and the user hasn't
        previously provided that permission, this will cause permission to be requested.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the scanning process, but will return *immediately*.
        The return value can be awaited in an asynchronous context, but cannot be used
        directly.

        :param device: The camera device to use for scanning. If ``None``, the default
            camera will be used.
        :param code_types: The types of barcodes to scan for. If ``None``, all supported
            types will be detected.
        :param on_detection: A handler to invoke when a barcode is detected. This can
            also be set via the :attr:`on_detection` property.
        :param continuous: If ``False`` (default), scanning stops after the first
            detection. If ``True``, scanning continues until :meth:`stop_scanning` is
            called.
        :returns: An asynchronous result; when awaited, returns the detected content
            string if a barcode was found, or ``None`` if scanning was cancelled.
        :raises PermissionError: if the app does not have permission to use the camera.
        """
        if on_detection is not None:
            self.on_detection = on_detection

        if code_types is None:
            code_types = list(BarcodeFormat)

        result = ScanResult(None)
        self._impl.start_scanning(
            result, device=device, code_types=code_types, continuous=continuous
        )
        return result

    def stop_scanning(self) -> None:
        """Stop scanning for barcodes.

        If the camera is currently scanning, the scan preview will be dismissed and the
        pending :class:`ScanResult` from :meth:`start_scanning` will resolve with
        ``None``.
        """
        self._impl.stop_scanning()
