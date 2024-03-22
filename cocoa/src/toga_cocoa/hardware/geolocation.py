from __future__ import annotations

from rubicon.objc import NSObject, objc_method, objc_property

from toga import LatLng

# for classes that need to be monkeypatched for testing
from toga_cocoa import libs as cocoa
from toga_cocoa.libs import (
    CLAuthorizationStatus,
    NSBundle,
)


class TogaLocationDelegate(NSObject):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def locationManagerDidChangeAuthorization_(self, manager) -> None:
        print("DID CHANGE AUTH STATUS", self.impl.native.authorizationStatus)
        self.impl._authorization_change()
        print("AUTH DONE")

    @objc_method
    def locationManager_didUpdateLocations_(self, manager, locations) -> None:
        print("DID UPDATE LOCATIONS")
        for location in locations:
            print(f" - {location.coordinate}")
            print(
                f" is {LatLng(location.coordinate.latitude, location.coordinate.longitude)}"
            )

        self.impl._location_change(locations[-1])
        print("UPDATE DONE")
        print()

    @objc_method
    def locationManager_didFailWithError_(self, manager, error) -> None:
        print("LOCATION MANAGER ERROR")
        print("error", error)
        self.impl._location_error(error)
        print("ERROR DONE")
        print()


class Geolocation:
    def __init__(self, interface):
        self.interface = interface
        if cocoa.CLLocationManager.locationServicesEnabled:
            print("Location services enabled")
            for key in [
                "CFBundleDisplayName",
                "CFBundleExecutable",
                "CFBundleIdentifier",
                "NSCameraUsageDescription",
                "NSLocationWhenInUseUsageDescription",
                "NSLocationAlwaysAndWhenInUseUsageDescription",
            ]:
                print(f"{key}={NSBundle.mainBundle.objectForInfoDictionaryKey(key)}")
            print("create manager")
            self.native = cocoa.CLLocationManager.alloc().init()
            print("manager exists")
            self.delegate = TogaLocationDelegate.alloc().init()
            self.native.delegate = self.delegate
            self.delegate.interface = interface
            self.delegate.impl = self
        else:
            raise PermissionError("Location services not enabled")
        self.permission_requests = []
        self.location_requests = []

    def _authorization_change(self):
        while self.permission_requests:
            future = self.permission_requests.pop()
            future.set_result(self.has_permission())

    def _location_change(self, location):
        latlng = LatLng(
            location.coordinate.latitude,
            location.coordinate.longitude,
        )

        # A vertical accuracy that non-positive indicates altitude is invalid.
        print(
            "ALT",
            location.altitude,
            location.ellipsoidalAltitude,
            location.verticalAccuracy,
        )
        if location.verticalAccuracy > 0.0:
            altitude = location.ellipsoidalAltitude
        else:
            altitude = None

        # Set all outstanding location requests with the most last location reported
        while self.location_requests:
            future = self.location_requests.pop()
            print("SET FUTURE")
            future.set_result(latlng)

        # Notify the change listener of the last location reported
        print("ON CHANGE")
        self.interface.on_change(
            location=latlng,
            altitude=altitude,
        )

    def _location_error(self, error):
        # Cancel all outstanding location requests.
        while self.location_requests:
            future = self.location_requests.pop()
            future.set_exception(RuntimeError(f"Unable to obtain a location ({error})"))

    def has_permission(self, allow_unknown=False):
        valid_values = {
            CLAuthorizationStatus.AuthorizedAlways.value,
            CLAuthorizationStatus.AuthorizedWhenInUse.value,
        }
        if allow_unknown:
            valid_values.add(CLAuthorizationStatus.NotDetermined.value)

        return self.native.authorizationStatus in valid_values

    def request_permission(self, future):
        self.permission_requests.append(future)
        # print("REQUEST IN USE")
        # self.native.requestWhenInUseAuthorization()
        print("REQUEST ALWAYS")
        self.native.requestAlwaysAuthorization()
        print("REQUESTED")

    def current_location(self, result):
        if self.has_permission(allow_unknown=True):
            location = self.native.location
            # print(
            #     "PREV LOCATION",
            #     location,
            # )
            # if location is None:
            #     self.location_requests.append(result)
            #     print("GET LOCATION USE")
            #     self.native.requestLocation()
            #     print("LOCATION REQUESTED")
            # else:
            result.set_result(
                LatLng(
                    location.coordinate.latitude,
                    location.coordinate.longitude,
                )
            )
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def start(self):
        if self.has_permission(allow_unknown=True):
            print("START UPDATES")
            self.native.startUpdatingLocation()
            print("STARTED")
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )

    def stop(self):
        if self.has_permission(allow_unknown=True):
            print("STOP UPDATES")
            self.native.stopUpdatingLocation()
            print("STOPPED")
        else:
            raise PermissionError(
                "App does not have permission to use geolocation services"
            )
