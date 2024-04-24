from unittest.mock import Mock

import pytest
from android import Manifest
from android.location import Location, LocationManager
from java.util import ArrayList

from toga_android.hardware.location import TogaLocationConsumer

from .hardware import HardwareProbe


class LocationProbe(HardwareProbe):
    def __init__(self, monkeypatch, app_probe):
        super().__init__(monkeypatch, app_probe.app)

        self._mock_LocationService = Mock()
        monkeypatch.setattr(
            app_probe.app.location._impl, "native", self._mock_LocationService
        )

        # The list of locations that will be in the next update
        self._locations = []

    def cleanup(self):
        # Delete the location service instance. This ensures that a freshly mocked
        # LocationManager is installed for each test.
        try:
            del self.app._location
        except AttributeError:
            pass

    def grant_permission(self):
        self._mock_permissions[Manifest.permission.ACCESS_COARSE_LOCATION] = 1
        self._mock_permissions[Manifest.permission.ACCESS_FINE_LOCATION] = 1

    def grant_background_permission(self):
        self._mock_permissions[Manifest.permission.ACCESS_BACKGROUND_LOCATION] = 1

    def allow_permission(self):
        self._mock_permissions[Manifest.permission.ACCESS_COARSE_LOCATION] = -1
        self._mock_permissions[Manifest.permission.ACCESS_FINE_LOCATION] = -1

    def allow_background_permission(self):
        self._mock_permissions[Manifest.permission.ACCESS_BACKGROUND_LOCATION] = -1

    def reject_permission(self):
        self._mock_permissions[Manifest.permission.ACCESS_COARSE_LOCATION] = 0
        self._mock_permissions[Manifest.permission.ACCESS_FINE_LOCATION] = 0

    def add_location(self, location, altitude, cached=False):
        native_location = Location(LocationManager.FUSED_PROVIDER)
        native_location.setLatitude(location.lat)
        native_location.setLongitude(location.lng)
        if altitude:
            native_location.setAltitude(altitude)

        self._locations.append(native_location)

    async def simulate_current_location(self, location):
        await self.redraw("Wait for current location")

        # There has been exactly 1 request to get the current location
        assert self._mock_LocationService.getCurrentLocation.call_count == 1
        call = self._mock_LocationService.getCurrentLocation.mock_calls[0]

        # Check some of the arguments invoking the location request
        assert call.args[0] == LocationManager.FUSED_PROVIDER
        assert isinstance(call.args[3], TogaLocationConsumer)

        # Stimulate the consumer associated with the update, using the
        # most recent location update
        call.args[3].accept(self._locations[-1])

        # Reset for the next call
        self._mock_LocationService.getCurrentLocation.reset_mock()

        # Reset the locations list.
        self._locations = []

        return await location

    async def simulate_location_update(self):
        await self.redraw("Wait for location update")

        # Trigger the listener. If there's only one known location, use it directly;
        # otherwise, pass them all in as a java List.
        if len(self._locations) == 1:
            locations = self._locations[0]
        else:
            locations = ArrayList()
            for location in self._locations:
                locations.add(location)
        self.app.location._impl.listener.onLocationChanged(locations)

        # Reset the locations list.
        self._locations = []

    async def simulate_location_error(self, location):
        await self.redraw("Wait for location error")

        pytest.xfail("Android's location service doesn't raise errors on failure")
