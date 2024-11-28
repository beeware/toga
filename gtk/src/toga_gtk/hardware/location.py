from __future__ import annotations

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
        self.native: Geoclue.Simple = None

        #: Handle ID for ``Geoclue.Simple`` location listener
        self.notify_location_handle: None | int = None

        #: Handle ID for client active notify listener
        self.notify_active_listener: None | int = None

        #: None if permissions are not requested, otherwise, indicates whether permissions are available
        self.permission_result: None | bool = None

    def _start(self):
        """Asynchronously initialize ``Geoclue.Simple``.

        The act of initializing ``Geoclue.Simple`` will itself trigger
        a permission request. As such, delay this until permission is checked.
        """
        self.props.state = State.STARTING

        Geoclue.Simple.new(
            self.interface.app.app_id,
            self.get_max_accuracy_level(),
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

    @property
    def is_sandboxed(self):
        return self.interface.app._impl.is_sandboxed

    def has_permission(self):
        return bool(self.permission_result)

    def request_permission(self, result):
        if self.permission_result is not None:
            result.set_result(self.permission_result)
            return

        if self.can_get_location:
            result.set_result(True)
            self.permission_result = True

        elif self.props.state < State.READY:
            if self.gsettings_disallow_location():
                self.props.state = State.DENIED
                result.set_result(False)
                self.permission_result = False
                return

            def wait_for_client(*args):
                if self.props.state < State.READY:
                    return

                self.permission_result = self.can_get_location
                result.set_result(self.can_get_location)
                self.disconnect(listener_handle)

            listener_handle = self.connect("notify::state", wait_for_client)

            if self.props.state == State.INITIAL:
                self._start()
        else:
            result.set_result(False)
            self.permission_result = False

    @property
    def gsettings_location(self):
        if self.is_sandboxed:
            # Sandboxed applications can read the org.gnome.system.location settings
            # but they will always be the default values
            # Therefore, ignore gsettings for sandboxed applications and instead rely
            # on XDG Portal's location permission handling
            return None

        if not hasattr(self, "_gsettings_location"):
            settings_schema_source = Gio.SettingsSchemaSource.get_default()
            location_setting_schema_id = "org.gnome.system.location"
            location_setting_available = settings_schema_source.lookup(
                location_setting_schema_id, recursive=False
            )

            if location_setting_available:
                self._gsettings_location = Gio.Settings.new(location_setting_schema_id)
            else:
                self._gsettings_location = None

        return self._gsettings_location

    def gsettings_disallow_location(self):
        return (settings := self.gsettings_location) and not settings.get_boolean(
            "enabled"
        )

    def get_max_accuracy_level(self) -> int:
        # match GSettings' and XDG Portal's default max accuracy levels
        DEFAULT_MAX_ACCURACY_LEVEL = Geoclue.AccuracyLevel.EXACT

        if settings := self.gsettings_location:
            # get as a string rather than enum int so we can avoid needing to import GDesktopEnums
            # and in turn rely on its system dependency
            gsettings_max_accuracy_level = settings.get_string(
                "max-accuracy-level"
            ).upper()
            return getattr(
                Geoclue.AccuracyLevel,
                gsettings_max_accuracy_level,
                DEFAULT_MAX_ACCURACY_LEVEL,
            )
        else:
            # There's no way to introspect the Portal permissions, so fall back to the default
            # without further checks
            return DEFAULT_MAX_ACCURACY_LEVEL

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
        """Start tracking Geoclue location updates.

        If state is anything other than READY, this method is a noop.

        The reason for this, for each other state is:
        - MONITORING: already monitoring, nothing to do
        - INITIAL: not possible because the upstream Location interface enforces a
            permission check, and the permission check starts Geoclue as part of
            permission checking
        - STARTING: not possible because permission check only finishes when Geoclue is
            ready or has reached a failure state
        - FAILED, DENIED: these are failure states; maybe an exception should be raised
        """
        if self.props.state == State.READY:
            self.notify_location_handle = self.native.connect(
                "notify::location", self.location_listener
            )
            self.props.state = State.MONITORING
            # Manually notify when connecting in order to propagate the initial location
            self.native.notify("location")

    def stop_tracking(self):
        """Stop tracking Geoclue location updates.

        If not currently tracking, this method is a noop.
        """
        if self.notify_location_handle is not None:
            self.native.disconnect(self.notify_location_handle)
            self.props.state = State.READY

    def current_location(self, location):
        """Asynchronously retrieve the current location.

        If state is anything other than READY or MONITORING, this method is a noop.

        See the docstring on :meth:`.Location.start_tracking()` regarding noop cases.
        All the same cases apply to this method, except for MONITORING, because the
        current location should be retrieved whenever Geoclue is available, even if the
        location is also being tracked.
        """
        if self.can_get_location:
            location.set_result(toga_location(self.native.get_location())["location"])
