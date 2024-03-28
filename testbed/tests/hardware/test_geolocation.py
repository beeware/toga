from unittest.mock import Mock

import pytest

from toga import LatLng

from ..conftest import skip_on_platforms
from .probe import get_probe


@pytest.fixture
async def geolocation_probe(monkeypatch, app_probe):
    skip_on_platforms("linux", "windows")
    probe = get_probe(monkeypatch, app_probe, "Geolocation")
    yield probe
    probe.cleanup()


async def test_grant_permission(app, geolocation_probe):
    """A user can grant permission to use geolocation."""
    # Prime the permission system to approve permission requests
    geolocation_probe.allow_permission()

    # Initiate the permission request. As permissions are primed, they will be approved.
    assert await app.geolocation.request_permission()

    # Permission now exists, but not background permission
    assert app.geolocation.has_permission
    assert not app.geolocation.has_background_permission

    # A second request to grant permissions is a no-op
    assert await app.geolocation.request_permission()

    # Permission still exists, but not background permission
    assert app.geolocation.has_permission
    assert not app.geolocation.has_background_permission


async def test_deny_permission(app, geolocation_probe):
    """A user can deny permission to use geolocation."""
    # Initiate the permission request. As permissions are not primed, they will be denied.
    assert not await app.geolocation.request_permission()

    # Permission has been denied
    assert not app.geolocation.has_permission
    assert not app.geolocation.has_background_permission

    # A second request to request permissions is a no-op
    assert not await app.geolocation.request_permission()

    # Permission is still denied
    assert not app.geolocation.has_permission
    assert not app.geolocation.has_background_permission


async def test_grant_background_permission(app, geolocation_probe):
    """A user can grant background permission to use geolocation."""
    # Prime the permission system to approve permission requests
    geolocation_probe.allow_background_permission()

    # Foreground permissions haven't been approved, so requesting background permissions
    # will raise an error
    with pytest.raises(
        PermissionError,
        match=(
            r"Cannot ask for background geolocation permission "
            r"before confirming foreground geolocation permission\."
        ),
    ):
        await app.geolocation.request_background_permission()

    # Pre-approve foreground permissions
    geolocation_probe.grant_permission()

    # Initiate the permission request. As permissions are primed, they will be approved.
    assert await app.geolocation.request_background_permission()

    # Permission now exists for both foreground and background
    assert app.geolocation.has_permission
    assert app.geolocation.has_background_permission

    # A second request to grant background permissions is a no-op
    assert await app.geolocation.request_background_permission()

    # Permission still exists for both foreground and background
    assert app.geolocation.has_permission
    assert app.geolocation.has_background_permission


async def test_deny_background_permission(app, geolocation_probe):
    """A user can deny background permission to use geolocation."""
    # Foreground permissions haven't been approved, so requesting background permissions
    # will raise an error.
    with pytest.raises(
        PermissionError,
        match=(
            r"Cannot ask for background geolocation permission "
            r"before confirming foreground geolocation permission\."
        ),
    ):
        await app.geolocation.request_background_permission()

    # Neither permission does not exist yet
    assert not app.geolocation.has_permission
    assert not app.geolocation.has_background_permission

    # Pre-approve foreground permissions
    geolocation_probe.grant_permission()

    # Initiate the permission request. As background permissions are not primed, they
    # will be denied.
    assert not await app.geolocation.request_background_permission()

    # Background permission has been denied, but foreground permission must exist
    assert app.geolocation.has_permission
    assert not app.geolocation.has_background_permission

    # A second request to request permissions is a no-op
    assert not await app.geolocation.request_background_permission()

    # Background permission is still denied, but foreground permission must exist
    assert app.geolocation.has_permission
    assert not app.geolocation.has_background_permission


async def test_current_location(app, geolocation_probe):
    """A user can take a photo with the all the available geolocations."""
    # Ensure geolocation has permissions
    geolocation_probe.grant_permission()

    # Install a change handler
    handler = Mock()
    app.geolocation.on_change = handler

    # Set the value that will be returned by the next location request
    expected_loc = LatLng(37, 42)
    expected_alt = 5

    geolocation_probe.add_location(expected_loc, expected_alt)

    # Request the current location
    location = app.geolocation.current_location()

    # Simulate a location update
    assert await geolocation_probe.simulate_current_location(location) == expected_loc

    # The on_change handler has been invoked
    handler.assert_called_once_with(
        app.geolocation,
        location=expected_loc,
        altitude=expected_alt,
    )

    handler.reset_mock()

    # Set the location as a cached value for the location service.
    # Some implementations may use this to optimize the returned value.
    # Make the altitude value indicating it is unreliable
    expected_loc = LatLng(42, 37)
    expected_alt = None

    geolocation_probe.add_location(expected_loc, expected_alt, cached=True)

    # Make another request for the location
    location = app.geolocation.current_location()

    # Simulate another location update
    assert await geolocation_probe.simulate_current_location(location) == expected_loc

    # The on_change handler has been invoked
    handler.assert_called_once_with(
        app.geolocation,
        location=expected_loc,
        altitude=expected_alt,
    )


async def test_track_location(app, geolocation_probe):
    """If the geolocation service raises an error, location requests raise an error."""
    # Ensure geolocation has permissions
    geolocation_probe.grant_permission()

    # Install a change handler
    handler = Mock()
    app.geolocation.on_change = handler

    # Start geolocation tracking
    app.geolocation.start()

    # Set a single location
    expected_loc = LatLng(37, 42)
    expected_alt = 5

    geolocation_probe.add_location(expected_loc, expected_alt)

    # Simulate a background location update
    await geolocation_probe.simulate_location_update()

    # The on_change handler has been invoked
    handler.assert_called_once_with(
        app.geolocation,
        location=expected_loc,
        altitude=expected_alt,
    )

    # Reset the mock
    handler.reset_mock()

    # Run the next update; this time, include 2 locations in the update.
    expected_loc = LatLng(42, 37)
    expected_alt = 5

    geolocation_probe.add_location(LatLng(0, 0), 0)
    geolocation_probe.add_location(expected_loc, expected_alt)

    # Simulate a background location update
    await geolocation_probe.simulate_location_update()

    # The on_change handler has been invoked once, with the most recent location
    handler.assert_called_once_with(
        app.geolocation,
        location=expected_loc,
        altitude=expected_alt,
    )

    # Stop geolocation tracking
    app.geolocation.stop()


async def test_geolocation_error(app, geolocation_probe):
    """If the geolocation service raises an error, location requests raise an error."""
    # Ensure geolocation has permissions
    geolocation_probe.grant_permission()

    # Set the value that will be returned by the next location request
    geolocation_probe.add_location(LatLng(37, 42), 5)

    # Request the current location
    location = app.geolocation.current_location()

    # Simulate a location update that raises an error
    with pytest.raises(RuntimeError, match=r"Unable to obtain a location \(.*\)"):
        assert await geolocation_probe.simulate_location_error(location)


async def test_no_permission(app, geolocation_probe):
    """If permissions have been denied, PermissionError is raised."""
    # Deny permission to use geolocation
    geolocation_probe.reject_permission()

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use geolocation services",
    ):
        await app.geolocation.current_location()

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use geolocation services",
    ):
        app.geolocation.start()

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use geolocation services",
    ):
        app.geolocation.stop()
