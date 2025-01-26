"""
GeoClue-based GTK location services.

For manually testing locations and location updates over time, consider using
the GeoClueless utility: https://gitlab.gnome.org/jwestman/geoclueless

Note: this utility must run with root privileges in order to register itself on the
system D-Bus in place of GeoClue, user discretion is advised!

Refer to repository README for setup instructions and dependencies. Then, from the
repository root, run the following to use GeoClueless's provided example, which tracks
location updates in a square around London, with an update every half second::

    sudo ./geoclueless.py --loop csv --rate=2 ./examples/london.csv

If you wish to avoid using GeoClueless, you may also mock location updates using
GeoClue's ``static`` location provider. Refer to ``man 5 geoclue`` for instructions
on how to enable the ``static`` location provider, as well as how to configure an
``/etc/geolocation`` file. The manpage includes example contents.

Changes to the coordinates in ``/etc/geolocation`` will be reflected in connected
GeoClue clients. That is, you can effectively test tracking location updates by
modifying the coordinates in the file, and that will propagate to any listening
process the same way a "real" location update would.
"""

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
    (Gio.DBusError.quark(), Gio.DBusError.ACCESS_DENIED),
]

if Flatpak is not None:
    KNOWN_PERMISSION_ERRORS.append(
        (Flatpak.PortalError.quark(), Flatpak.PortalError.NOT_ALLOWED),
    )
else:  # pragma: no cover
    # Non-sandboxed and no Flatpak library installed. That's a valid system
    # configuration, but there's no meaningful way to test it; it can just be ignored
    pass


def is_permissions_error(error):
    """Determine if a ``GLib.Error`` is one of the known GeoClue permissions errors.

    If GeoClue version <= 2.7.2 is in use, these permissions errors will not surface
    due to a (now resolved) bug in ``Geoclue.Simple``'s error handling
    https://gitlab.freedesktop.org/geoclue/geoclue/-/issues/205

    In that case, the error will be a generic IO Failure, so permission failures
    will be indistinguishable from other systemic failures.

    :param error: a GLib.Error instance
    :returns: whether the error is one of the known permissions errors
    """
    return any(
        error.matches(error_domain, error_code)
        for error_domain, error_code in KNOWN_PERMISSION_ERRORS
    )


class State(IntEnum):
    INITIAL = auto()
    """GeoClue has not been started."""

    STARTING = auto()
    """Waiting for the GeoClue client to finish starting."""

    READY = auto()
    """GeoClue is ready to retrieve the location."""

    MONITORING = auto()
    """Actively monitoring the location."""

    FAILED = auto()
    """GeoClue was unable to retrieve the location due to a generic error."""

    DENIED = auto()
    """Location access was denied to the application."""

    @classmethod
    def is_available(cls, state):
        return State.READY <= state <= State.MONITORING

    @classmethod
    def is_uninitialised(cls, state):
        return state <= State.STARTING


class Location(GObject.Object):
    #: State of GeoClue location service initialisation and communication
    state = GObject.Property(type=int, default=State.INITIAL)

    def __init__(self, interface):
        if Geoclue is None:
            # CI (where coverage is enforced) must always have GeoClue available
            # in order to perform the rest of the tests
            raise RuntimeError(  # pragma: no cover
                "Unable to import GeoClue. Ensure that the system package "
                "providing GeoClue and its GTK bindings have been installed. See "
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
                self.props.state = State.DENIED
            else:
                self.props.state = State.FAILED

            return
        else:
            self.props.state = State.READY

        client = self.native.get_client()
        # GeoClue docs indicate a client proxy is not used in sandboxed environments
        # https://gitlab.freedesktop.org/geoclue/geoclue/-/blob/master/libgeoclue/gclue-simple.c?ref_type=heads#L978-979
        if client:

            def notify_client_active(*args):
                if not self.native.get_client().props.active:
                    # If the client explicitly becomes inactive, this indicates
                    # a failure to retrieve the location
                    # e.g., when the geoclue service is stopped on the host
                    self.props.state = State.FAILED
                    self._stop_tracking()
                else:  # pragma: no cover
                    # Not possible to meaningfully test in a platform agnostic manner
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

        def wait_for_client(*args):
            if State.is_uninitialised(self.props.state):  # pragma: no cover
                return

            # See note on :func:`~.is_permission_error` regarding error ambiguity
            # for some Geoclue versions. Because of this ambiguity any initialisation
            # failure needs to be communicated as permissions issue, and ``result``
            # cannot reliably be set to an exception if state is FAILED instead of
            # DENIED.
            self.permission_result = State.is_available(self.props.state)

            result.set_result(self.permission_result)
            self.disconnect(listener_handle)

        listener_handle = self.connect("notify::state", wait_for_client)

        if self.props.state == State.INITIAL:
            self._start()
        else:  # pragma: no cover
            # This cannot be tested because the test probe runs a sync initialisation
            # There is no method by which initialisation can be triggered in the test
            # environment and then permissions requested before initialisation finishes
            # In other words, there is no situation in test where the status is starting
            pass

    def has_background_permission(self):
        """Check for background permission.

        Background location permission has no meaning for GeoClue,
        as all location access is mediated through the same location
        tracking APIs. Therefore, background location permission
        is handled in identical terms to foreground location permission.
        """
        return self.has_permission()

    def request_background_permission(self, result):
        """Request background permission.

        Due to the reasons outlined in :meth:`~.Location.has_background_permission()`
        which mean that GeoClue background permission exactly mirrors the state of
        foreground permissions, as well Toga core's implementation of
        ``request_background_permission``, which requires foreground permission to be
        requested first and never calls this method on the implementation class if
        background permission is granted, it is impossible for this method to ever
        actually run in real usage.

        Because of this, it must be marked with a ``no cover`` pragma, as the testbed
        has no platform agnostic way to exercise this method, and testing it at all
        be meaningless, as it is not intended to be used anyway.
        """
        result.set_result(None)  # pragma: no cover

    def location_listener(self, *args):
        self.interface.on_change(**toga_location(self.native.get_location()))

    def start_tracking(self):
        """Start tracking GeoClue location updates."""
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
                "Unable to start tracking (location service is unavailable)"
            )

    def _stop_tracking(self) -> bool:
        """If monitoring, stop tracking.

        :return bool: Whether tracking was stopped"""
        if self.notify_location_handle is not None:
            self.native.disconnect(self.notify_location_handle)
            return True
        return False

    def stop_tracking(self):
        """Stop tracking GeoClue location updates.

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
