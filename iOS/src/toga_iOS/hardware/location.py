from __future__ import annotations

from rubicon.objc import NSObject, objc_method, objc_property

from toga import LatLng
from toga.constants import LocationMode

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
    def locationManager_didVisit_(self, manager, visit) -> None:
        """
        Handles visit events and sends detailed data to the API.
        """
        latitude = visit.coordinate().latitude
        longitude = visit.coordinate().longitude
        arrival_time = visit.arrivalDate().timeIntervalSince1970
        departure_time = (
            visit.departureDate().timeIntervalSince1970
            if visit.departureDate()
            else None
        )
        accuracy = visit.horizontalAccuracy  # Accuracy of visit detection

        loc = LatLng(latitude, longitude)

        if self.interface.on_change:
            self.interface.on_change(
                location=loc,
                altitude=None,
                type="visit",
                arrival_time=arrival_time,
                departure_time=departure_time,
                accuracy=accuracy,
            )

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
            self.tracking_mode = None

        else:  # pragma: no cover
            # The app doesn't have the NSLocationWhenInUseUsageDescription key (e.g.,
            # via `permission.*_location` in Briefcase). No-cover because we can't
            # manufacture this condition in testing.
            raise RuntimeError(
                "Application metadata does not declare that "
                "the app will use the camera."
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
                    "Application metadata does not declare that "
                    "the app will use the camera."
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
        self.tracking_mode = LocationMode.CONTINUOUS
        self.native.startUpdatingLocation()

    def start_significant_tracking(self) -> None:
        """Start monitoring significant location changes."""
        # Ensure that background processing will occur
        self.native.allowsBackgroundLocationUpdates = True
        self.native.pausesLocationUpdatesAutomatically = False

        self._is_tracking = True
        self.tracking_mode = LocationMode.SIGNIFICANT
        self.native.startMonitoringSignificantLocationChanges()

    def start_visit_tracking(self) -> None:
        """Start monitoring visits (CLVisit events)."""
        # Ensure that background processing will occur
        self.native.allowsBackgroundLocationUpdates = True
        self.native.pausesLocationUpdatesAutomatically = False

        self._is_tracking = True
        self.tracking_mode = LocationMode.VISITS
        self.native.startMonitoringVisits()

    def stop_tracking(self):
        self._is_tracking = False
        if self.tracking_mode == LocationMode.CONTINUOUS:
            self.native.stopUpdatingLocation()
        elif self.tracking_mode == LocationMode.SIGNIFICANT:
            self.native.stopMonitoringSignificantLocationChanges()
        elif self.tracking_mode == LocationMode.VISITS:
            self.native.stopMonitoringVisits()
        else:
            return
