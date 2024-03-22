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
        :param altitude: The user's altitude in meters above WGS84 reference ellipsoid.
            Returns None if the altitude could not be determined.
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
    def on_change(self) -> OnLocationChangeHandler:
        """The handler to invoke when the user's location changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)

    def start(self):
        """Start monitoring the user's location for changes.

        An :any:`on_change` callback will be generated then when the user's location
        changes.
        """
        self._impl.start()

    def stop(self):
        """Stop monitoring the user's location."""
        self._impl.stop()

    @property
    def current_location(self) -> LocationResult:
        """Obtain the user's current location using the geolocation service.

        If the platform requires permission to access the geolocation service, and the
        user hasn't previously provided that permission, this will cause permission to
        be requested.

        **This is an asynchronous property**. If you request this property in
        synchronous context, it will start the process of requesting the user's
        location, but will return *immediately*. The return value can be awaited in an
        asynchronous context, but cannot be compared directly.

        :returns: An asynchronous result; when awaited, returns the :any:`toga.Image`
            captured by the camera, or ``None`` if the photo was  cancelled.
        """
        location = LocationResult(None)
        self._impl.current_location(location)
        return location
