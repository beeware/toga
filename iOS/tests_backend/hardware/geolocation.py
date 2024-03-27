from unittest.mock import Mock, PropertyMock

from rubicon.objc import ObjCClass

from toga_iOS import libs as iOS
from toga_iOS.libs import (
    CLAuthorizationStatus,
    CLLocationCoordinate2D,
)

from ..app import AppProbe

CLLocation = ObjCClass("CLLocation")
NSDate = ObjCClass("NSDate")
NSError = ObjCClass("NSError")


class GeolocationProbe(AppProbe):
    def __init__(self, monkeypatch, app_probe):
        super().__init__(app_probe.app)

        self.monkeypatch = monkeypatch

        # The mocked permission. A negative value indicates that permission *would*
        # be granted if requested but, has not been granted *yet*. Unless primed,
        # permissions will be denied.
        self._mock_permission = None
        self._mock_background_permission = None

        # Mock CLLocationManager
        self._mock_location_manager = Mock()

        # Mock the CLLocationManager.authorizationStatus property
        def _mock_auth_status():
            if self._mock_background_permission == 1:
                return CLAuthorizationStatus.AuthorizedAlways.value
            elif self._mock_permission == 1:
                return CLAuthorizationStatus.AuthorizedWhenInUse.value
            elif self._mock_permission == 0:
                return CLAuthorizationStatus.Denied.value
            else:
                return CLAuthorizationStatus.NotDetermined.value

        type(self._mock_location_manager).authorizationStatus = PropertyMock(
            side_effect=_mock_auth_status
        )

        # Mock CLLocationManager.requestWhenInUseAuthorization and
        # CLLocationManager.requestAlwaysAuthorization
        def _mock_request_when_in_use():
            if self._mock_permission is None:
                self._mock_permission = 0
            else:
                self._mock_permission = abs(self._mock_permission)
            # Trigger delegate handling for permission change
            self.app.geolocation._impl.delegate.locationManagerDidChangeAuthorization(
                None
            )

        def _mock_request_always():
            if self._mock_background_permission is None:
                self._mock_background_permission = 0
            else:
                self._mock_background_permission = abs(self._mock_background_permission)

            # Trigger delegate handling for permission change
            self.app.geolocation._impl.delegate.locationManagerDidChangeAuthorization(
                None
            )

        self._mock_location_manager.requestWhenInUseAuthorization = (
            _mock_request_when_in_use
        )
        self._mock_location_manager.requestAlwaysAuthorization = _mock_request_always

        # Mock the CLLocationManager.location shortcut; depends on this probe having
        # `._location` being set by the `set_location()` method.
        def _mock_location():
            try:
                loc, cached = self._location
                if cached:
                    return loc
                return None
            except AttributeError:
                raise Exception("current location hasn't been primed")

        type(self._mock_location_manager).location = PropertyMock(
            side_effect=_mock_location
        )

        # Mock the alloc().init() call chain that returns a CLLocationManager instance
        self._mock_CLLocationManager = Mock()
        cl_alloc = Mock()
        cl_alloc.init = Mock(return_value=self._mock_location_manager)
        self._mock_CLLocationManager.alloc = Mock(return_value=cl_alloc)
        monkeypatch.setattr(iOS, "CLLocationManager", self._mock_CLLocationManager)

    def cleanup(self):
        # Delete the geolocation service instance. This ensures that a freshly mocked
        # CLLocationManager is installed for each test.
        try:
            del self.app._geolocation
        except AttributeError:
            pass

    def reset_permission(self):
        self._mock_permissions = None

    def grant_permission(self):
        self._mock_permission = -1

    def grant_background_permission(self):
        self._mock_background_permission = -1

    def allow_permission(self):
        self._mock_permission = 1

    def allow_background_permission(self):
        self._mock_background_permission = 1

    def reject_permission(self):
        self._mock_permission = 0

    def set_location(self, location, altitude, cached=False):
        self._location = (
            CLLocation.alloc().initWithCoordinate(
                CLLocationCoordinate2D(location.lat, location.lng),
                altitude=0.0 if altitude is None else altitude,
                horizontalAccuracy=10.0,
                verticalAccuracy=-1.0 if altitude is None else 2.0,
                timestamp=NSDate.now(),
            ),
            cached,
        )

    async def simulate_location_update(self, location):
        await self.redraw("Wait for geolocation update")

        next_loc, cached = self._location
        if cached:
            # If we can use the cached update, a request won't be issued
            self.app.geolocation._impl.native.requestLocation.assert_not_called()
        else:
            # A location request was issued
            self.app.geolocation._impl.native.requestLocation.assert_called_once_with()
            self.app.geolocation._impl.native.requestLocation.reset_mock()

            # Trigger the callback, providing 2 locations; only the second one will be
            # used.
            self.app.geolocation._impl.delegate.locationManager(
                None,
                didUpdateLocations=[
                    CLLocation.alloc().initWithCoordinate(
                        CLLocationCoordinate2D(0.0, 0.0),
                        altitude=0.0,
                        horizontalAccuracy=10.0,
                        verticalAccuracy=-1.0,
                        timestamp=NSDate.now(),
                    ),
                    next_loc,
                ],
            )

        return await location

    async def simulate_location_error(self, location):
        await self.redraw("Wait for geolocation error")

        self.app.geolocation._impl.native.requestLocation.assert_called_once_with()
        self.app.geolocation._impl.native.requestLocation.reset_mock()

        # Trigger the error handler
        self.app.geolocation._impl.delegate.locationManager(
            None,
            didFailWithError=NSError.errorWithDomain(
                "Geolocation", code=42, userInfo=None
            ),
        )

        return await location
