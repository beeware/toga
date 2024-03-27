from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

import toga
from toga.handlers import AsyncResult, PermissionResult, wrapped_handler
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.app import App


class LocationResult(AsyncResult):
    RESULT_TYPE = "location"


class OnLocationChangeHandler(Protocol):
    def __call__(
        self,
        geolocation: Geolocation,
        location: toga.LatLng,
        altitude: float | None,
        **kwargs: Any,
    ) -> None:
        """A handler that will be invoked when the user's location changes.

        :param geolocation: the Geolocation service that generated the update.
        :param location: The user's location as (latitude, longitude).
        :param altitude: The user's altitude in meters above mean sea level. Returns
            None if the altitude could not be determined.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """
        ...


class Geolocation:
    def __init__(self, app: App):
        self.factory = get_platform_factory()
        self._app = app
        self._impl = self.factory.Geolocation(self)

        self.on_change = None

    @property
    def app(self) -> App:
        """The app with which the geolocation service is associated"""
        return self._app

    @property
    def has_permission(self) -> bool:
        """Does the app have permission to use geolocation services?

        If the platform requires the user to explicitly confirm permission, and
        the user has not yet given permission, this will return ``False``.
        """
        return self._impl.has_permission()

    def request_permission(self) -> PermissionResult:
        """Request sufficient permissions to capture the user's location.

        If permission has already been granted, this will return without prompting the
        user.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the process of requesting permissions, but will return
        *immediately*. The return value can be awaited in an asynchronous context, but
        cannot be compared directly.

        :returns: An asynchronous result; when awaited, returns True if the app has
            permission to capture the user's a geolocation; False otherwise.
        """
        result = PermissionResult(None)

        if has_permission := self.has_permission:
            result.set_result(has_permission)
        else:
            self._impl.request_permission(result)

        return result

    @property
    def has_background_permission(self) -> bool:
        """Does the app have permission to use geolocation services in the background?

        If the platform requires the user to explicitly confirm permission, and the user
        has not yet given permission, this will return ``False``.
        """
        return self._impl.has_background_permission()

    def request_background_permission(self) -> PermissionResult:
        """Request sufficient permissions to capture the user's location in the
        background.

        If permission has already been granted, this will return without prompting the
        user.

        **This is an asynchronous method**. If you invoke this method in synchronous
        context, it will start the process of requesting permissions, but will return
        *immediately*. The return value can be awaited in an asynchronous context, but
        cannot be compared directly.

        :returns: An asynchronous result; when awaited, returns True if the app has
            permission to capture the user's a geolocation while running in the
            background; False otherwise.
        """
        result = PermissionResult(None)

        if has_background_permission := self.has_background_permission:
            result.set_result(has_background_permission)
        else:
            self._impl.request_background_permission(result)

        return result

    @property
    def on_change(self) -> OnLocationChangeHandler:
        """The handler to invoke when an update to the user's location is available."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)

    def start(self):
        """Start monitoring the user's location for changes.

        An :any:`on_change` callback will be generated then when the user's location
        changes.

        :raises PermissionError: If the app has not requested and received permission to
            use geolocation services.
        """
        if self.has_permission:
            self._impl.start()
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def stop(self):
        """Stop monitoring the user's location.

        :raises PermissionError: If the app has not requested and received permission to
            use geolocation services.
        """
        if self.has_permission:
            self._impl.stop()
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def current_location(self) -> LocationResult:
        """Obtain the user's current location using the geolocation service.

        If the app hasn't requested and received permission to use geolocation, a
        :any:`PermissionError` will be raised.

        **This is an asynchronous method**. If you call this method in a synchronous
        context, it will start the process of requesting the user's location, but will
        return *immediately*. The return value can be awaited in an asynchronous
        context, but cannot be compared directly.

        If an :any:`on_change` handler is installed, requesting the current location
        will also cause that handler to be invoked.

        :returns: An asynchronous result; when awaited, returns the :any:`toga.Image`
            captured by the camera, or ``None`` if the photo was  cancelled.
        :raises PermissionError: If the app has not requested and received permission to
            use geolocation services.
        """
        location = LocationResult(None)
        if self.has_permission:
            self._impl.current_location(location)
        else:
            location.set_exception(
                PermissionError(
                    "App does not have permission to use geolocation services"
                )
            )
        return location
