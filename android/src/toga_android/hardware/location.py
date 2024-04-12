from __future__ import annotations

from android import Manifest
from android.content import Context
from android.content.pm import PackageManager
from android.location import LocationListener, LocationManager
from android.os import Build
from java import dynamic_proxy
from java.util import List
from java.util.function import Consumer

from toga import LatLng


def toga_location(location):
    """Convert an Android location into a Toga LatLng and altitude."""
    latlng = LatLng(location.getLatitude(), location.getLongitude())

    # MSL altitude was added in API 34. We can't test this at runtime
    if Build.VERSION.SDK_INT >= 34 and location.hasMslAltitude():  # pragma: no cover
        altitude = location.getMslAltitudeMeters()
    elif location.hasAltitude():
        altitude = location.getAltitude()
    else:
        altitude = None

    return {
        "location": latlng,
        "altitude": altitude,
    }


class TogaLocationConsumer(dynamic_proxy(Consumer)):
    def __init__(self, impl, result):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface
        self.result = result

    def accept(self, location):
        loc = toga_location(location)
        self.result.set_result(loc["location"])


class TogaLocationListener(dynamic_proxy(LocationListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def onLocationChanged(self, location):
        if isinstance(location, List):
            location = location.get(location.size() - 1)

        self.interface.on_change(**toga_location(location))


class Location:
    def __init__(self, interface):
        self.interface = interface
        self.context = self.interface.app._impl.native.getApplicationContext()
        if not any(
            self.context.getPackageManager().hasSystemFeature(feature)
            for feature in [
                PackageManager.FEATURE_LOCATION,
                PackageManager.FEATURE_LOCATION_GPS,
                PackageManager.FEATURE_LOCATION_NETWORK,
            ]
        ):  # pragma: no cover
            # The app doesn't have a feature supporting location services. No-cover
            # because we can't manufacture this condition in testing.
            raise RuntimeError("Location services are not available on this device.")

        self.native = self.context.getSystemService(Context.LOCATION_SERVICE)
        self.listener = TogaLocationListener(self)

    def has_permission(self):
        return (
            self.interface.app._impl._native_checkSelfPermission(
                Manifest.permission.ACCESS_COARSE_LOCATION
            )
            == PackageManager.PERMISSION_GRANTED
        ) or (
            self.interface.app._impl._native_checkSelfPermission(
                Manifest.permission.ACCESS_FINE_LOCATION
            )
            == PackageManager.PERMISSION_GRANTED
        )

    def has_background_permission(self):
        return (
            self.interface.app._impl._native_checkSelfPermission(
                Manifest.permission.ACCESS_BACKGROUND_LOCATION
            )
            == PackageManager.PERMISSION_GRANTED
        )

    def request_permission(self, future):
        def request_complete(permissions, results):
            # Map the permissions to their result
            perms = dict(zip(permissions, results))
            try:
                result = (
                    perms[Manifest.permission.ACCESS_COARSE_LOCATION]
                    == PackageManager.PERMISSION_GRANTED
                ) or (
                    perms[Manifest.permission.ACCESS_FINE_LOCATION]
                    == PackageManager.PERMISSION_GRANTED
                )
            except KeyError:  # pragma: no cover
                # This shouldn't ever happen - we shouldn't get a completion of a
                # location permission request that doesn't include location permissions
                # - but just in case, we'll assume if it's not there, it failed.
                result = False
            future.set_result(result)

        self.interface.app._impl.request_permissions(
            [
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_FINE_LOCATION,
            ],
            on_complete=request_complete,
        )

    def request_background_permission(self, future):
        def request_complete(permissions, results):
            # Map the permissions to their result
            perms = dict(zip(permissions, results))
            try:
                result = (
                    perms[Manifest.permission.ACCESS_BACKGROUND_LOCATION]
                    == PackageManager.PERMISSION_GRANTED
                )
            except KeyError:  # pragma: no cover
                # This shouldn't ever happen - we shouldn't get a completion of a
                # location permission request that doesn't include location permissions
                # - but just in case, we'll assume if it's not there, it failed.
                result = False
            future.set_result(result)

        self.interface.app._impl.request_permissions(
            [
                Manifest.permission.ACCESS_BACKGROUND_LOCATION,
            ],
            on_complete=request_complete,
        )

    def current_location(self, result):
        consumer = TogaLocationConsumer(self, result)
        self.native.getCurrentLocation(
            LocationManager.FUSED_PROVIDER,
            None,
            self.context.getMainExecutor(),
            consumer,
        )

    def start_tracking(self):
        # Start updates, with pings no more often than every 5 seconds, or 10 meters.
        self.native.requestLocationUpdates(
            LocationManager.FUSED_PROVIDER,
            5000,
            10,
            self.listener,
        )

    def stop_tracking(self):
        self.native.removeUpdates(self.listener)
