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
        altitude = location.ellipsoidalAltitude
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
        self.impl._authorization_change()

    @objc_method
    def locationManager_didUpdateLocations_(self, manager, locations) -> None:
        self.impl._location_change(locations[-1])

    @objc_method
    def locationManager_didFailWithError_(self, manager, error) -> None:
        self.impl._location_error(error)


class Geolocation:
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
        else:
            raise RuntimeError(
                "Application metadata does not declare that the app will use the camera."
            )

        # Tracking of futures associated with specific requests.
        self.permission_requests = []
        self.current_location_requests = []

    def _authorization_change(self):
        while self.permission_requests:
            future = self.permission_requests.pop()
            future.set_result(self.has_permission())

    def _location_change(self, location):
        toga_loc = toga_location(location)

        # Set all outstanding location requests with location reported
        while self.current_location_requests:
            future = self.current_location_requests.pop()
            future.set_result(toga_loc["location"])

        # Notify the change listener of the last location reported
        self.interface.on_change(**toga_loc)

    def _location_error(self, error):
        # Cancel all outstanding location requests.
        while self.current_location_requests:
            future = self.current_location_requests.pop()
            future.set_exception(RuntimeError(f"Unable to obtain a location ({error})"))

    def has_permission(self):
        return self.native.authorizationStatus in {
            CLAuthorizationStatus.AuthorizedAlways.value,
            CLAuthorizationStatus.AuthorizedWhenInUse.value,
        }

    def has_background_permission(self):
        return (
            self.native.authorizationStatus
            == CLAuthorizationStatus.AuthorizedAlways.value
        )

    def request_permission(self, future):
        self.permission_requests.append(future)
        self.native.requestWhenInUseAuthorization()

    def request_background_permission(self, future):
        if NSBundle.mainBundle.objectForInfoDictionaryKey(
            "NSLocationAlwaysAndWhenInUseUsageDescription"
        ):
            self.permission_requests.append(future)

            self.native.requestAlwaysAuthorization()
        else:
            future.set_exception(
                RuntimeError(
                    "Application metadata does not declare that the app will use the camera."
                )
            )

    def current_location(self, result):
        if self.has_permission():
            location = self.native.location
            if location is None:
                self.current_location_requests.append(result)
                self.native.requestLocation()
            else:
                toga_loc = toga_location(location)
                result.set_result(toga_loc["location"])
                self.interface.on_change(**toga_loc)
        else:
            result.set_exception(
                PermissionError(
                    "App does not have permission to use geolocation services"
                )
            )

    def start(self):
        if self.has_permission():
            # Ensure that background processing will occur
            self.native.allowsBackgroundLocationUpdates = True
            self.native.pausesLocationUpdatesAutomatically = False

            self.native.startUpdatingLocation()
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def stop(self):
        if self.has_permission():
            self.native.stopUpdatingLocation()
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )
