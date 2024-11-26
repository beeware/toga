from enum import IntEnum, auto

import gi

from toga import LatLng
from toga_gtk.libs import Gio, GLib, GObject

gi.require_version("Geoclue", "2.0")
from gi.repository import Geoclue  # noqa: E402


def toga_location(location):
    """Convert a ``Geoclue.Location`` into ``OnLocationChangeHandler`` kwargs."""
    latlng = LatLng(*location.get_properties("latitude", "longitude"))
    altitude = location.get_property("altitude")

    return {
        "location": latlng,
        "altitude": altitude,
    }


class States(IntEnum):
    STARTING = auto()
    """Waiting for the Geoclue client to initialise."""

    READY = auto()
    """Geoclue is ready to connect."""

    MONITORING = auto()
    """Actively monitoring the location."""

    FAILED = auto()
    """``Geoclue`` was unable to retrieve the location due to a generic error."""

    DENIED = auto()
    """Permission to read the location was denied."""


class Location(GObject.Object):
    # Implement as GObject.Object to allow notifying on state changes within the event loop
    state = GObject.Property(type=int, default=States.STARTING)

    def __init__(self, interface):
        super().__init__()

        self.interface = interface

        self.geoclue_simple = None
        self.notify_location_handle = None
        self.notify_active_listener = None
        self.in_flatpak = None

        def new_finish(_, async_result):
            try:
                self.geoclue_simple = Geoclue.Simple.new_finish(async_result)
            except GLib.Error as e:
                if e.matches(Gio.DBusError, Gio.DBusError.ACCESS_DENIED):
                    # TODO: In practice, I cannot get this to occur. Maybe it is KDE's portal
                    # implementation, but when I deny location permissions in the prompt,
                    # the failure is a generic DBusError.FAILED, not a permission denied
                    # failure.
                    self.props.state = States.DENIED
                else:
                    self.props.state = States.FAILED
                    print("Failed to get location", e.message, e.code)

                return
            else:
                self.props.state = States.READY

            client = self.geoclue_simple.get_client()
            # Geoclue docs indicate a client proxy is not used in Flatpak
            # https://lazka.github.io/pgi-docs/#Geoclue-2.0/classes/Simple.html#Geoclue.Simple.props.client
            self.in_flatpak = client is None

            if client:

                def notify_client_active(*args):
                    if not self.geoclue_simple.get_client().props.active:
                        # If the client explicitly becomes inactive, this indicates
                        # a failure to retrieve the location
                        self.props.state = States.DENIED

                self.notify_active_listener = client.connect(
                    "notify::active", notify_client_active
                )

        Geoclue.Simple.new(
            self.interface.app.app_id, Geoclue.AccuracyLevel.EXACT, None, new_finish
        )

    @property
    def can_get_location(self):
        return self.props.state in (States.READY, States.MONITORING)

    def has_permission(self):
        # TODO: Think this through a bit more
        if self.props.state == States.STARTING:
            # Cannot know whether permission request is needed...
            # False is safe?
            return False

        if self.in_flatpak and not self.can_get_location:
            # In flatpak, explicit permission required
            return False

        # Otherwise, no explicit permission required
        return True

    def request_permission(self, result):
        if self.can_get_location:
            result.set_result(True)
        elif self.props.state == States.STARTING:

            def wait_for_client(*args):
                result.set_result(self.can_get_location)
                self.disconnect(listener_handle)

            listener_handle = self.connect("notify::state", wait_for_client)
        else:
            result.set_result(False)

    def has_background_permission(self):
        return self.has_permission()

    def request_background_permission(self, result):
        self.request_permission(result)

    def start_tracking(self):
        self.notify_location_handle = self.geoclue_simple.connect(
            "notify::location", self.location_listener
        )
        self.props.state = States.MONITORING
        # Manually notify when connecting to get the initial location
        self.location_listener()

    def stop_tracking(self):
        self.geoclue_simple.disconnect(self.notify_location_handle)
        self.props.state = States.READY

    def location_listener(self, *args):
        self.interface.on_change(**toga_location(self.geoclue_simple.get_location()))

    def current_location(self, location):
        location.set_result(**toga_location(self.geoclue_simple.get_location()))
