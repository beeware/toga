from unittest.mock import Mock

from pytest import xfail
from System.Device.Location import (
    GeoCoordinate,
    GeoCoordinateWatcher,
    GeoPositionPermission,
)

from toga.types import LatLng

from .hardware import HardwareProbe


class LocationProbe(HardwareProbe):
    supports_background_permission = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app.location._impl.watcher = Mock(spec=GeoCoordinateWatcher)
        self.reset_locations()

    def cleanup(self):
        # Delete the location service instance. This ensures that a freshly mocked
        # LocationManager is installed for each test.
        try:
            del self.app._location
        except AttributeError:
            pass

    def allow_permission(self):
        self.app.location._impl.watcher.Permission = GeoPositionPermission.Granted

    def grant_permission(self):
        self.app.location._impl.watcher.Permission = GeoPositionPermission.Granted

    def reject_permission(self):
        self.app.location._impl.watcher.Permission = GeoPositionPermission.Denied

    def add_location(self, location: LatLng, altitude, cached=False):
        m = Mock(spec=GeoCoordinate)
        m.Position = Mock()
        m.Position.Location = Mock()
        m.Position.Location.IsUnknown = False
        m.Position.Location.Latitude = location.lat
        m.Position.Location.Longitude = location.lng
        m.Position.Location.Altitude = altitude

        self._locations.append(m)
        self.app.location._impl.watcher.Position = m.Position

    def reset_locations(self):
        self._locations = []

    def allow_background_permission(self):
        """
        winforms doesn't distinguish between foreground and background access
        """
        pass

    async def simulate_location_error(self, loco):
        await self.redraw("Wait for location error")

        xfail("Winforms's location service doesn't raise errors on failure")

    async def simulate_current_location(self, location):
        await self.redraw("Wait for current location")

        self.reset_locations()

        return await location

    async def simulate_location_update(self):
        self.app.location._impl._position_changed(None, self._locations[-1])
