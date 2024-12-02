from unittest.mock import Mock

from pytest import xfail

from toga.types import LatLng

from .hardware import HardwareProbe


class LocationProbe(HardwareProbe):
    def cleanup(self):
        # Delete the location service instance. This ensures that a freshly mocked
        # LocationManager is installed for each test.
        try:
            del self.app._location
        except AttributeError:
            pass

    def allow_permissions(self):
        pass

    def allow_permission(self):
        pass

    def grant_permission(self):
        self.app.location._has_permission = True

    def reject_permission(self):
        xfail("No support for permissions here")

    def add_location(self, location: LatLng, altitude, cached=False):
        m = Mock()
        m.Position = Mock()
        m.Position.Location = Mock()
        m.Position.Location.Latitude = location.lat
        m.Position.Location.Longitude = location.lng
        m.Position.Location.Altitude = altitude

        self.app.location._impl._position_changed(None, m)

    def allow_background_permission(self):
        pass

    async def simulate_location_error(self, loco):
        raise RuntimeError(f"Unable to obtain a location ({loco})")

    async def simulate_current_location(self, loco):
        res = await loco
        assert res is not None
        return res

    async def simulate_location_update(self):
        pass
