"""
TODO
"""

from collections import defaultdict
from unittest.mock import Mock
from weakref import WeakSet

import pytest

from toga_gtk.hardware.location import State as LocationState
from toga_gtk.libs import Geoclue, GLib

from ..app import AppProbe


class MockGeoclueSimple:
    def __init__(self):
        self._mock_error = None
        self._connected_handlers = defaultdict(dict)
        self._handler_locations = defaultdict(WeakSet)
        self.location = None

    def set_error(self, domain, code):
        self._mock_error = GLib.Error.new_literal(domain, "whoops", code)

    def get_location(self):
        return self.location

    def new(self, app_id, accuracy, cancellable, callback):
        callback(None, self)

    def new_finish(self, async_result):
        if self._mock_error is not None:
            raise self._mock_error

        return async_result

    def get_client(self): ...

    def notify(self, property):
        # Only notifies handlers if they haven't already received an update
        # for the currently set location
        if self.location is None:
            # Cannot notify an empty location
            return

        message = f"notify::{property}"
        for handler_id, handler in self._connected_handlers[message].items():
            if self.location in self._handler_locations[handler_id]:
                pass

            handler()
            self._handler_locations[handler_id].add(self.location)

    def connect(self, message, handler):
        handler_id = hash(handler)
        self._connected_handlers[message][handler_id] = handler
        return handler_id

    def disconnect(self, handler_id):
        for handlers in self._connected_handlers.values():
            if handler_id in handlers:
                handlers.pop(handler_id)
                break
        else:
            raise ValueError(f"{handler_id} is not a valid testing handler ID")


class LocationProbe(AppProbe):
    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.mock_error = None
        self.mock_geoclue_simple = MockGeoclueSimple()
        self.mock_geoclue_simple.get_location = Mock(
            wraps=self.mock_geoclue_simple.get_location
        )

        monkeypatch.setattr(Geoclue, "Simple", self.mock_geoclue_simple)

        self.app.location._impl.props.state = LocationState.DENIED

    def cleanup(self):
        try:
            del self.app._location
        except AttributeError:
            pass

    def grant_permission(self):
        self.allow_permission()
        self.app.location._impl._start()

    def grant_background_permission(self):
        self.allow_background_permission()
        self.app.location._impl._start()

    def allow_permission(self):
        self.app.location._impl.permission_requested = True

    def allow_background_permission(self):
        self.app.location._impl.background_permission_requested = True

    def reject_permission(self):
        self.app.location._impl.props.state = LocationState.DENIED

    def add_location(self, location, altitude, cached=False):
        # Geoclue only deals with a single location, so the
        # list-of-locations that other testbeds implement isn't necessary here
        geoclue_location = Geoclue.LocationSkeleton.new()
        geoclue_location.props.latitude = location.lat
        geoclue_location.props.longitude = location.lng
        geoclue_location.props.altitude = altitude if altitude is not None else 0

        self.mock_geoclue_simple.location = geoclue_location

    async def simulate_current_location(self, location):
        await self.redraw("Wait for current location")

        self.mock_geoclue_simple.get_location.assert_called_once()
        self.mock_geoclue_simple.get_location.reset_mock()

        return await location

    async def simulate_location_update(self):
        await self.redraw("Wait for location update")

        self.mock_geoclue_simple.notify("location")

        self.mock_geoclue_simple.get_location.assert_called_once()
        self.mock_geoclue_simple.get_location.reset_mock()

    async def simulate_location_error(self, _):
        await self.redraw("Wait for location error")

        pytest.xfail("Geoclue will not notify if location detection fails.")
