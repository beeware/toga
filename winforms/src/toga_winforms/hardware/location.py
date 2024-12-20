from __future__ import annotations

from contextlib import contextmanager

from System import EventHandler
from System.Device.Location import (
    GeoCoordinate,
    GeoCoordinateWatcher,
    GeoPositionAccuracy,
    GeoPositionChangedEventArgs,
    GeoPositionPermission,
)

from toga import LatLng
from toga.handlers import AsyncResult


def toga_location(location: GeoCoordinate):
    """Convert a GeoCoordinate into a Toga LatLng and altitude."""

    if location.IsUnknown:
        return None

    return {
        "location": LatLng(location.Latitude, location.Longitude),
        "altitude": location.Altitude,
    }


class Location:
    def __init__(self, interface):
        self.interface = interface
        self.watcher = GeoCoordinateWatcher(GeoPositionAccuracy.Default)
        self._handler = EventHandler[GeoPositionChangedEventArgs[GeoCoordinate]](
            self._position_changed
        )
        self._tracking = False
        self._has_background_permission = False
        self.watcher.OnPropertyChanged = self._property_changed

    def _property_changed(self, property_name: str):
        if property_name == "Permission":
            # TODO: handle permission changes
            print("PERMISSION CHANGED", self.watcher.Permission)

    def _position_changed(
        self,
        sender: GeoCoordinateWatcher,
        event: GeoPositionChangedEventArgs[GeoCoordinate],
    ):
        location = toga_location(event.Position.Location)
        if location:
            self.interface.on_change(**location)

    def has_permission(self):
        return self.watcher.Permission == GeoPositionPermission.Granted

    def has_background_permission(self):
        return self._has_background_permission

    @contextmanager
    def context(self):
        if not self._tracking:
            self.watcher.Start(False)
        try:
            yield
        finally:
            if not self._tracking:  # don't want to stop if we're tracking
                self.watcher.Stop()

    def request_permission(self, future: AsyncResult[bool]) -> None:
        with self.context():
            future.set_result(self.has_permission())

    def request_background_permission(self, future: AsyncResult[bool]) -> None:
        if not self.has_permission():
            raise PermissionError()
        future.set_result(True)
        self._has_background_permission = True

    def current_location(self, result: AsyncResult[dict]) -> None:
        def cb(sender, event):
            if (
                event.Position.Location.IsUnknown
                or event.Position.Location.HorizontalAccuracy > 100
            ):
                return
            self.watcher.remove_PositionChanged(cb)
            loco = toga_location(event.Position.Location)
            result.set_result(loco["location"] if loco else None)
            ctx.__exit__()

        ctx = self.context()

        ctx.__enter__()

        self.watcher.add_PositionChanged(
            EventHandler[GeoPositionChangedEventArgs[GeoCoordinate]](cb)
        )

    def start_tracking(self) -> None:
        self.watcher.Start()
        self.watcher.add_PositionChanged(self._handler)
        self._tracking = True

    def stop_tracking(self) -> None:
        self.watcher.Stop()
        self.watcher.remove_PositionChanged(self._handler)
        self._tracking = False
