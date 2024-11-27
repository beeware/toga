from enum import IntEnum, auto

from toga import LatLng
from toga_gtk.libs import Geoclue, Gio, GLib, GObject


def toga_location(location):
    """Convert a ``Geoclue.Location`` into ``OnLocationChangeHandler`` kwargs."""
    latlng = LatLng(location.props.latitude, location.props.longitude)
    altitude = location.get_property("altitude")

    return {
        "location": latlng,
        "altitude": altitude,
    }


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

    DENIED = auto()
    """Permission to read the location was denied."""


class Location(GObject.Object):
    #: State of Geoclue location service initialisation and communication
    state = GObject.Property(type=int, default=State.INITIAL)

    def __init__(self, interface):
        if Geoclue is None:
            raise RuntimeError(
                "Unable to import Geoclue. Ensure that the system package "
                "providing Geoclue and its GTK bindings have been installed. "
                "See https://toga.readthedocs.io/en/stable/reference/api/hardware/location.html#system-requirements "
                "for details."
            )

        super().__init__()

        self.interface = interface

        #: ``Geoclue.Simple`` instance
        self.native = None

        #: Handle ID for ``Geoclue.Simple`` location listener
        self.notify_location_handle = None

        #: Handle ID for client active notify listener
        self.notify_active_listener = None

        #: Whether permissions have been requested
        self.permission_requested = False

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
            if e.matches(Gio.DBusError, Gio.DBusError.ACCESS_DENIED):
                # TODO: In practice, I cannot get this to occur. Maybe it is KDE's portal
                # implementation, but when I deny location permissions in the prompt,
                # the failure is a generic DBusError.FAILED, not a permission denied
                # failure.
                self.props.state = State.DENIED
            else:
                self.props.state = State.FAILED
                print("Failed to get location", e.message, e.code)

            return
        else:
            self.props.state = State.READY

        client = self.native.get_client()
        # Geoclue docs indicate a client proxy is not used in sandboxed environments
        # https://lazka.github.io/pgi-docs/#Geoclue-2.0/classes/Simple.html#Geoclue.Simple.props.client
        if client:

            def notify_client_active(*args):
                if not self.native.get_client().props.active:
                    # If the client explicitly becomes inactive, this indicates
                    # a failure to retrieve the location
                    self.props.state = State.DENIED

            self.notify_active_listener = client.connect(
                "notify::active", notify_client_active
            )

    @property
    def can_get_location(self):
        """Whether ``Geoclue.Simple`` is ready to provide a location."""
        return self.props.state in (State.READY, State.MONITORING)

    def has_permission(self):
        return self.permission_requested and self.can_get_location

    def request_permission(self, result):
        if self.can_get_location:
            result.set_result(True)
            self.permission_requested = True

        elif self.props.state < State.READY:

            def wait_for_client(*args):
                if self.props.state < State.READY:
                    return

                result.set_result(self.can_get_location)
                self.disconnect(listener_handle)

                self.permission_requested = True

            listener_handle = self.connect("notify::state", wait_for_client)

            if self.props.state == State.INITIAL:
                self._start()
        else:
            result.set_result(False)

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

        See documentation on :meth:`~toga_gtk.hardware.location.Location.has_background_permission()`
        for implementation details.
        """
        self.request_permission(result)

    def start_tracking(self):
        self.notify_location_handle = self.native.connect(
            "notify::location", self.location_listener
        )
        self.props.state = State.MONITORING
        # Manually notify when connecting in order to propagate the initial location
        self.native.notify("location")

    def stop_tracking(self):
        self.native.disconnect(self.notify_location_handle)
        self.props.state = State.READY

    def location_listener(self, *args):
        self.interface.on_change(**toga_location(self.native.get_location()))

    def current_location(self, location):
        location.set_result(toga_location(self.native.get_location())["location"])
