"""
TODO
"""

from collections import defaultdict
from unittest.mock import Mock
from weakref import WeakSet

import pytest

from toga_gtk.libs import Geoclue, Gio

from ..app import AppProbe


class MockGeoclueSimple:
    def __init__(self):
        self._connected_handlers = defaultdict(dict)
        self._handler_locations = defaultdict(WeakSet)
        self.location = None

    def get_location(self):
        return self.location

    def new(self, app_id, accuracy, cancellable, callback):
        callback(None, self)

    def new_finish(self, async_result):
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
    supports_background_permission = False

    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.mock_native = MockGeoclueSimple()
        self.mock_native.get_location = Mock(wraps=self.mock_native.get_location)

        monkeypatch.setattr(Geoclue, "Simple", self.mock_native)

        gio_settings_new = Gio.Settings.new

        self.mock_gsettings_location = Mock(
            wraps=gio_settings_new("org.gnome.system.location")
        )

        def mock_gio_settings_new(schema_id):
            if schema_id == "org.gnome.system.location":
                return self.mock_gsettings_location

            else:
                return gio_settings_new(Gio.Settings, schema_id)

        monkeypatch.setattr(Gio.Settings, "new", mock_gio_settings_new)

        # Start with a permission-rejecting posture
        self.reject_permission()

    def cleanup(self):
        try:
            del self.app._location
        except AttributeError:
            pass

    def grant_permission(self):
        self.allow_permission()
        self.app.location._impl.permission_result = True
        # grant must set up a realistic "already checked and granted" scenario
        # which for Geoclue necessitates starting Geoclue
        # In the real Geoclue.Simple, the start process is asynchronous
        # but ``MockGeoclueSimple.new()`` will be used here, which immediately
        # executes the callback chain, meaning this finishes synchronously in test
        self.app.location._impl._start()

    def grant_background_permission(self):
        self.grant_permission()

    def allow_permission(self):
        self.mock_gsettings_location.get_boolean.return_value = True

    def allow_background_permission(self):
        self.allow_permission()

    def reject_permission(self):
        self.mock_gsettings_location.get_boolean.return_value = False

    def add_location(self, location, altitude, cached=False):
        # Geoclue only deals with a single location, so the
        # list-of-locations that other testbeds implement isn't necessary here
        geoclue_location = Geoclue.LocationSkeleton.new()
        geoclue_location.props.latitude = location.lat
        geoclue_location.props.longitude = location.lng
        geoclue_location.props.altitude = altitude if altitude is not None else 0

        self.mock_native.location = geoclue_location

    async def simulate_current_location(self, location):
        await self.redraw("Wait for current location")

        self.mock_native.get_location.assert_called_once()
        self.mock_native.get_location.reset_mock()

        return await location

    async def simulate_location_update(self):
        await self.redraw("Wait for location update")

        self.mock_native.notify("location")

        self.mock_native.get_location.assert_called_once()
        self.mock_native.get_location.reset_mock()

    async def simulate_location_error(self, _):
        await self.redraw("Wait for location error")

        pytest.xfail("Geoclue will not notify if location detection fails.")
