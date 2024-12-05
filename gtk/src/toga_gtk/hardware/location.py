from __future__ import annotations

from enum import IntEnum, auto

from toga import LatLng
from toga_gtk.libs import Flatpak, Geoclue, Gio, GLib, GObject


def toga_location(location):
    """Convert a ``Geoclue.Location`` into ``OnLocationChangeHandler`` kwargs."""
    latlng = LatLng(location.props.latitude, location.props.longitude)
    altitude = location.get_property("altitude")

    return {
        "location": latlng,
        "altitude": altitude,
    }


KNOWN_PERMISSION_ERRORS = [
    (Gio.DBusError, Gio.DBusError.ACCESS_DENIED),
]

if Flatpak is not None:
    KNOWN_PERMISSION_ERRORS.append(
        (Flatpak.PortalError, Flatpak.PortalError.NOT_ALLOWED),
    )


def is_permissions_error(error):
    """Determine if a ``GLib.Error`` is one of the known Geoclue permissions errors.

    In practice, these permissions errors may not occur due to a bug in
    ``Geoclue.Simple``'s error handling
    https://gitlab.freedesktop.org/geoclue/geoclue/-/issues/205

    :param error: a GLib.Error instance
    :returns: whether the error is one of the known permissions errors
    """
    return any(
        error.matches(error_type, error_code)
        for error_type, error_code in KNOWN_PERMISSION_ERRORS
    )


class State(IntEnum):
    INITIAL = auto()
    """Geoclue has not been started."""

    STARTING = auto()
    """Waiting for the Geoclue client to finish starting."""

    READY = auto()
    """Geoclue is ready to connect."""

    MONITORING = auto()
    """Actively monitoring the location."""

    FAILED = auto()
    """``Geoclue`` was unable to retrieve the location due to a generic error."""

    @classmethod
    def is_available(cls, state):
        return State.READY <= state <= State.MONITORING

    @classmethod
    def is_errored(cls, state):
        return state == State.FAILED

    @classmethod
    def is_uninitialised(cls, state):
        return State.INITIAL <= state <= State.STARTING


class Location(GObject.Object):
    #: State of Geoclue location service initialisation and communication
    state = GObject.Property(type=int, default=State.INITIAL)

    def __init__(self, interface):
        if Geoclue is None:
            raise RuntimeError(
                "Unable to import Geoclue. Ensure that the system package "
                "providing Geoclue and its GTK bindings have been installed. See "
                "https://toga.readthedocs.io/en/stable/reference/api/hardware/location.html#system-requirements "  # noqa: E501
                "for details."
            )

        super().__init__()

        self.interface = interface

        #: ``Geoclue.Simple`` instance
        self.native: Geoclue.Simple = None

        #: Handle ID for ``Geoclue.Simple`` location listener
        self.notify_location_handle: None | int = None

        #: Handle ID for client active notify listener
        self.notify_active_listener: None | int = None

        self.permission_result: None | bool = None

    def _start(self):
        """Asynchronously initialize ``Geoclue.Simple``.

        The act of initializing ``Geoclue.Simple`` will itself trigger
        a permission request. As such, delay this until permission is checked.
        """
        self.props.state = State.STARTING

        Geoclue.Simple.new(
            self.interface.app.app_id,
            Geoclue.AccuracyLevel.EXACT,
            None,
            self._new_finish,
        )

    def _new_finish(self, _, async_result):
        try:
            self.native = Geoclue.Simple.new_finish(async_result)
        except GLib.Error as e:
            if is_permissions_error(e):
                self.permission_result = False

            self.props.state = State.FAILED

            return
        else:
            self.props.state = State.READY

        client = self.native.get_client()
        # Geoclue docs indicate a client proxy is not used in sandboxed environments
        # https://gitlab.freedesktop.org/geoclue/geoclue/-/blob/master/libgeoclue/gclue-simple.c?ref_type=heads#L978-979
        if client:

            def notify_client_active(*args):
                if not self.native.get_client().props.active:
                    # If the client explicitly becomes inactive, this indicates
                    # a failure to retrieve the location
                    # e.g., when the geoclue service is stopped on the host
                    self.props.state = State.FAILED
                    self._stop_tracking()
                else:
                    self.props.state = State.READY

            self.notify_active_listener = client.connect(
                "notify::active", notify_client_active
            )

    def has_permission(self):
        return bool(self.permission_result)

    def request_permission(self, result):
        if self.permission_result is not None:
            result.set_result(self.permission_result)
            return

        if State.is_uninitialised(self.props.state):

            def wait_for_client(*args):
                if State.is_uninitialised(self.props.state):  # pragma: no cover
                    return

                self.permission_result = State.is_available(self.props.state)
                result.set_result(self.permission_result)
                self.disconnect(listener_handle)

            listener_handle = self.connect("notify::state", wait_for_client)

            if self.props.state == State.INITIAL:
                self._start()

        else:
            result.set_result(State.is_available(self.props.state))

    def has_background_permission(self):
        """Check for background permission.

        Background location permission has no meaning for Geoclue,
        as all location access is mediated through the same location
        tracking APIs. Therefore, background location permission
        is handled in identical terms to foreground location permission.
        """
        return self.has_permission()

    def request_background_permission(self, result):
        """Request background permission.

        See documentation on :meth:`~.Location.has_background_permission()`
        for implementation details.
        """
        self.request_permission(result)

    def location_listener(self, *args):
        self.interface.on_change(**toga_location(self.native.get_location()))

    def start_tracking(self):
        """Start tracking Geoclue location updates."""
        if self.props.state == State.READY:
            self.notify_location_handle = self.native.connect(
                "notify::location", self.location_listener
            )
            self.props.state = State.MONITORING
            # Manually notify when connecting in order to propagate the initial location
            self.native.notify("location")
        elif self.props.state == State.MONITORING:
            # Already monitoring, noop
            pass
        else:
            raise RuntimeError(
                "Unable to obtain a location (location service is unavailable)"
            )

    def _stop_tracking(self) -> bool:
        """If monitoring, stop tracking.

        :return bool: Whether tracking was stopped"""
        if self.notify_location_handle is not None:
            self.native.disconnect(self.notify_location_handle)
            return True
        return False

    def stop_tracking(self):
        """Stop tracking Geoclue location updates.

        If not currently tracking, this method is a noop.
        """
        if self._stop_tracking():
            self.props.state = State.READY

    def current_location(self, location):
        """Asynchronously retrieve the current location."""
        if State.is_available(self.props.state):
            location.set_result(toga_location(self.native.get_location())["location"])
        else:
            location.set_exception(
                RuntimeError(
                    "Unable to obtain a location (location service is unavailable)"
                )
            )
