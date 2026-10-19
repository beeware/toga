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

    altitude = location.altitude if location.verticalAccuracy > 0 else None
    return {"location": latlng, "altitude": altitude}


def toga_visit(visit):
    """Convert a Cocoa visit into a Toga LatLng and structured data."""
    latlng = LatLng(
        visit.coordinate.latitude,
        visit.coordinate.longitude,
    )

    return {
        "location": latlng,
        "arrivalDate": visit.arrivalDate,
        "departureDate": visit.departureDate or None,
        "accuracy": visit.horizontalAccuracy,
    }


class TogaLocationDelegate(NSObject):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    # ------------------------------------------------------------------
    # Permission changes
    # ------------------------------------------------------------------
    @objc_method
    def locationManagerDidChangeAuthorization_(self, manager) -> None:
        while self.impl.permission_requests:
            future, permission = self.impl.permission_requests.pop()
            future.set_result(permission())

    # ------------------------------------------------------------------
    # Location updates (standard *and* opportunistic)
    # ------------------------------------------------------------------
    @objc_method
    def locationManager_didUpdateLocations_(self, manager, locations) -> None:
        toga_loc = toga_location(locations[-1])

        # Resolve any pending one‑shot requests
        while self.impl.current_location_requests:
            future = self.impl.current_location_requests.pop()
            future.set_result(toga_loc["location"])

        # Forward to app callback if tracking flag is set
        if self.impl._is_tracking:
            self.interface.on_change(**toga_loc)

    # ------------------------------------------------------------------
    # Visit updates
    # ------------------------------------------------------------------
    @objc_method
    def locationManager_didVisit_(self, manager, visit) -> None:
        visit_data = toga_visit(visit)
        if self.interface.on_visit:
            self.interface.on_visit(
                location=visit_data["location"],
                altitude=None,
                type="visit",
                arrival_time=visit_data["arrivalDate"].timeIntervalSince1970(),
                departure_time=(
                    visit_data["departureDate"].timeIntervalSince1970()
                    if visit_data["departureDate"]
                    else None
                ),
                accuracy=visit_data["accuracy"],
            )

    # ------------------------------------------------------------------
    # Error handler
    # ------------------------------------------------------------------
    @objc_method
    def locationManager_didFailWithError_(self, manager, error) -> None:
        while self.impl.current_location_requests:
            future = self.impl.current_location_requests.pop()
            future.set_exception(
                RuntimeError(f"Unable to obtain location ({error})")
            )


# ======================================================================
# Location backend (iOS)
# ======================================================================

class Location:
    """Original Toga iOS Location, plus *opportunistic* pig‑back listener."""

    def __init__(self, interface):
        self.interface = interface

        if not NSBundle.mainBundle.objectForInfoDictionaryKey(
            "NSLocationWhenInUseUsageDescription"
        ):
            raise RuntimeError(
                "Application metadata lacks NSLocationWhenInUseUsageDescription key."
            )

        # Primary manager (standard, SLC, visits)
        self.native = iOS.CLLocationManager.alloc().init()
        self.delegate = TogaLocationDelegate.alloc().init()
        self.native.delegate = self.delegate
        self.delegate.interface = interface
        self.delegate.impl = self

        # NEW: holder for ultra‑low‑power listener
        self._passive_mgr = None

        self._is_tracking = False
        self.significant = False

        # Futures tracking
        self.permission_requests = []
        self.current_location_requests = []

    # ------------------------------------------------------------------
    # Permission helpers
    # ------------------------------------------------------------------
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
        else:
            future.set_exception(
                RuntimeError(
                    "Info.plist missing NSLocationAlwaysAndWhenInUseUsageDescription"
                )
            )

    # ------------------------------------------------------------------
    # One‑shot current location
    # ------------------------------------------------------------------
    def current_location(self, result):
        loc = self.native.location
        if loc is None:
            self.current_location_requests.append(result)
            self.native.requestLocation()
        else:
            result.set_result(toga_location(loc)["location"])

    # ------------------------------------------------------------------
    # High‑accuracy continuous tracking
    # ------------------------------------------------------------------
    def start_tracking(self):
        self.native.allowsBackgroundLocationUpdates = True
        self.native.pausesLocationUpdatesAutomatically = False

        self._is_tracking = True
        self.significant = False
        self.native.startUpdatingLocation()

    def stop_tracking(self):
        self._is_tracking = False
        if not self.significant:
            self.native.stopUpdatingLocation()
        else:
            self.native.stopMonitoringSignificantLocationChanges()

    # ------------------------------------------------------------------
    # Significant‑change + Visit monitoring
    # ------------------------------------------------------------------
    def start_significant_tracking(self):
        self.native.allowsBackgroundLocationUpdates = True
        self.native.pausesLocationUpdatesAutomatically = False

        self._is_tracking = True
        self.significant = True
        self.native.startMonitoringSignificantLocationChanges()

    def start_visit_tracking(self):
        self.native.allowsBackgroundLocationUpdates = True
        self.native.pausesLocationUpdatesAutomatically = False

        self._is_tracking = True
        self.native.startMonitoringVisits()

    # ------------------------------------------------------------------
    # NEW – Opportunistic listener (zero‑cost pig‑back)
    # ------------------------------------------------------------------
    def start_opportunistic_tracking(self):
        """Receive *every* fix Core Location produces for any app without
        powering GPS ourselves (desiredAccuracy = 3 km). Call once after
        "Always" permission is granted."""
        if self._passive_mgr is not None:
            return  # already running

        mgr = iOS.CLLocationManager.alloc().init()
        mgr.delegate = self.delegate  # share same delegate
        mgr.desiredAccuracy = 3000.0  # kCLLocationAccuracyThreeKilometers
        mgr.distanceFilter = 0        # kCLDistanceFilterNone – deliver all fixes
        mgr.activityType = 6          # CLActivityTypeOtherNavigation
        mgr.allowsBackgroundLocationUpdates = True
        mgr.pausesLocationUpdatesAutomatically = True
        mgr.startUpdatingLocation()

        self._passive_mgr = mgr
        print("[iOS] Opportunistic listener started.")

    def stop_opportunistic_tracking(self):
        if self._passive_mgr is not None:
            self._passive_mgr.stopUpdatingLocation()
            self._passive_mgr = None
            print("[iOS] Opportunistic listener stopped.")
