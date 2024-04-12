from __future__ import annotations

from rubicon.objc import NSObject, objc_method, objc_property

from toga import LatLng

# for classes that need to be monkeypatched for testing
from toga_iOS import libs as iOS
from toga_iOS.libs import (
    CLAuthorizationStatus,
    NSBundle,
)


def toga_location(location):
    """Convert a Cocoa location into a Toga LatLng and altitude."""
    latlng = LatLng(
        location.coordinate.latitude,
        location.coordinate.longitude,
    )

    # A vertical accuracy that non-positive indicates altitude is invalid.
    if location.verticalAccuracy > 0.0:
        altitude = location.altitude
    else:
        altitude = None

    return {
        "location": latlng,
        "altitude": altitude,
    }


class TogaLocationDelegate(NSObject):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def locationManagerDidChangeAuthorization_(self, manager) -> None:
        while self.impl.permission_requests:
            future, permission = self.impl.permission_requests.pop()
            future.set_result(permission())

    @objc_method
    def locationManager_didUpdateLocations_(self, manager, locations) -> None:
        # The API *can* send multiple locations in a single update; they should be
        # sorted chronologically; only propagate the most recent one
        toga_loc = toga_location(locations[-1])

        # Set all outstanding location requests with location reported
        while self.impl.current_location_requests:
            future = self.impl.current_location_requests.pop()
            future.set_result(toga_loc["location"])

        # If we're tracking, notify the change listener of the last location reported
        if self.impl._is_tracking:
            self.interface.on_change(**toga_loc)

    @objc_method
    def locationManager_didFailWithError_(self, manager, error) -> None:
        # Cancel all outstanding location requests.
        while self.impl.current_location_requests:
            future = self.impl.current_location_requests.pop()
            future.set_exception(RuntimeError(f"Unable to obtain a location ({error})"))


class Location:
    def __init__(self, interface):
        self.interface = interface
        if NSBundle.mainBundle.objectForInfoDictionaryKey(
            "NSLocationWhenInUseUsageDescription"
        ):
            self.native = iOS.CLLocationManager.alloc().init()
            self.delegate = TogaLocationDelegate.alloc().init()
            self.native.delegate = self.delegate
            self.delegate.interface = interface
            self.delegate.impl = self
            self._is_tracking = False

        else:  # pragma: no cover
            # The app doesn't have the NSLocationWhenInUseUsageDescription key (e.g.,
            # via `permission.*_location` in Briefcase). No-cover because we can't
            # manufacture this condition in testing.
            raise RuntimeError(
                "Application metadata does not declare that the app will use the camera."
            )

        # Tracking of futures associated with specific requests.
        self.permission_requests = []
        self.current_location_requests = []

    def has_permission(self):
        return self.native.authorizationStatus in {
            CLAuthorizationStatus.AuthorizedWhenInUse.value,
            CLAuthorizationStatus.AuthorizedAlways.value,
        }

    def has_background_permission(self):
        return (
            self.native.authorizationStatus
            == CLAuthorizationStatus.AuthorizedAlways.value
        )

    def request_permission(self, future):
        self.permission_requests.append((future, self.has_permission))
        self.native.requestWhenInUseAuthorization()

    def request_background_permission(self, future):
        if NSBundle.mainBundle.objectForInfoDictionaryKey(
            "NSLocationAlwaysAndWhenInUseUsageDescription"
        ):
            self.permission_requests.append((future, self.has_background_permission))

            self.native.requestAlwaysAuthorization()
        else:  # pragma: no cover
            # The app doesn't have the NSLocationAlwaysAndWhenInUseUsageDescription key
            # (e.g., via `permission.background_location` in Briefcase). No-cover
            # because we can't manufacture this condition in testing.
            future.set_exception(
                RuntimeError(
                    "Application metadata does not declare that the app will use the camera."
                )
            )

    def current_location(self, result):
        location = self.native.location
        if location is None:
            self.current_location_requests.append(result)
            self.native.requestLocation()
        else:
            toga_loc = toga_location(location)
            result.set_result(toga_loc["location"])

    def start_tracking(self):
        # Ensure that background processing will occur
        self.native.allowsBackgroundLocationUpdates = True
        self.native.pausesLocationUpdatesAutomatically = False

        self._is_tracking = True
        self.native.startUpdatingLocation()

    def stop_tracking(self):
        self.native.stopUpdatingLocation()
        self._is_tracking = False
