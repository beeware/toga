"""
Location probes for Toga GTK.

See :mod:`toga_gtk.hardware.location` docstring for details on why multiple distinct
probe implementations are required.
"""

import os
from collections import defaultdict
from unittest.mock import Mock
from weakref import WeakSet

import pytest

from toga_gtk.libs import Geoclue, Gio, GLib, GObject

from ..app import AppProbe


class MockClient(GObject.Object):
    active = GObject.Property(type=bool, default=True)


class MockGeoclueSimple:
    def __init__(self):
        self._connected_handlers = defaultdict(dict)
        self._handler_locations = defaultdict(WeakSet)
        self.creation_error = None
        self.location = None
        self.client = MockClient()

    def get_location(self):
        return self.location

    def new(self, app_id, accuracy, cancellable, callback):
        callback(None, self)

    def new_finish(self, async_result):
        if self.creation_error is not None:
            raise self.creation_error

        return async_result

    def get_client(self):
        return self.client

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
        self._verify_dependencies()
        super().__init__(app_probe.app)

        self.mock_native = MockGeoclueSimple()
        self.mock_native.get_location = Mock(wraps=self.mock_native.get_location)

        monkeypatch.setattr(Geoclue, "Simple", self.mock_native)

        self.mock_native.creation_error = GLib.Error.new_literal(
            Gio.DBusError.quark(),
            f"{self.app.app_id} disallowed by configuration for UID 1000",
            Gio.DBusError.ACCESS_DENIED,
        )

    def _verify_dependencies(self):
        if os.getenv("CI", None) is not None:
            assert (
                Geoclue is not None
            ), "libgeoclue dependency is required to run location tests on linux"
        elif Geoclue is None:
            pytest.xfail(
                "Linux location tests require libgeoclue, but it was not available"
            )

    def cleanup(self):
        try:
            del self.app._location
        except AttributeError:
            pass

    def allow_permission(self):
        self.mock_native.creation_error = None

    def allow_background_permission(self):
        self.allow_permission()

    def reject_permission(self):
        self.mock_native.creation_error = GLib.Error.new_literal(
            Gio.DBusError.quark(),
            f"{self.app.app_id} disallowed by configuration for UID 1000",
            Gio.DBusError.ACCESS_DENIED,
        )
        self.app.location._impl._start()

    def grant_permission(self):
        self.allow_permission()
        self.app.location._impl.permission_result = True
        # grant must set up a realistic "already checked and granted" scenario
        # which for GeoClue necessitates starting GeoClue
        # In the real ``Geoclue.Simple``, the start process is asynchronous
        # but ``MockGeoclueSimple.new()`` will be used here, which immediately
        # executes the callback chain, meaning this finishes synchronously in test
        self.app.location._impl._start()

    def grant_background_permission(self):
        self.grant_permission()

    def add_location(self, location, altitude, cached=False):
        # GeoClue only deals with a single location, so the
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

    def setup_location_error(self):
        self.mock_native.client.props.active = False

    def setup_tracking_start_error(self):
        self.mock_native.client.props.active = False

    async def simulate_location_error(self, location):
        # No simulation required after setup_location_error, wait for the location
        # future to complete and return the result for the testbed to use
        return await location


class SandboxedLocationProbe(LocationProbe):
    def __init__(self, monkeypatch, app_probe):
        super().__init__(monkeypatch, app_probe)

        # The operative difference for sandboxed applications is the lack of client
        # proxy usage by ``Geoclue.Simple``
        self.mock_native.client = None

    def reject_permission(self):
        # Due to a bug in the ``Geoclue.Simple`` implementation,
        # https://gitlab.freedesktop.org/geoclue/geoclue/-/issues/205,
        # permissions errors in sandboxed contexts are flattened to a generic IO error
        # That provides a convenient place to ensure tests cover the fallback
        # error case during ``Geoclue.Simple`` instantiation
        self.mock_native.creation_error = GLib.Error.new_literal(
            Gio.io_error_quark(), "Start failed", Gio.IOErrorEnum.FAILED
        )
        self.app.location._impl._start()

    def _xfail_location_portal_no_post_init_failure(self):
        pytest.xfail(
            "XDG Location Portal does not fail after initialisation "
            "(which occurs during and is required by permissions)"
        )

    def setup_tracking_start_error(self):
        self._xfail_location_portal_no_post_init_failure()

    def setup_location_error(self):
        self._xfail_location_portal_no_post_init_failure()


PROBES = (LocationProbe, SandboxedLocationProbe)
