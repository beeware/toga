import contextlib
from unittest.mock import Mock

import pytest

import toga
from toga_dummy import factory
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
)


def test_no_location(monkeypatch, app):
    """If there's no location service, and no factory implementation, accessing camera raises an
    exception."""
    try:
        monkeypatch.delattr(app, "_location")
    except AttributeError:
        pass
    monkeypatch.delattr(factory, "Location")

    # Accessing the location object should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        app.location


@pytest.mark.parametrize(
    "initial, should_request, has_permission",
    [
        (-2, True, True),
        (-1, True, True),
        (0, True, False),
        (1, False, True),
        (2, False, True),
    ],
)
def test_request_permission(app, initial, should_request, has_permission):
    """An app can request permission to use location."""
    # The location instance round-trips the app instance
    assert app.location.app == app

    # Set initial permission
    app.location._impl._has_permission = initial

    assert (
        app.loop.run_until_complete(app.location.request_permission()) == has_permission
    )

    if should_request:
        assert_action_performed(app.location, "request permission")
        assert_action_not_performed(app.location, "request background permission")
    else:
        assert_action_not_performed(app.location, "request permission")
        assert_action_not_performed(app.location, "request background permission")

    # As a result of requesting, location permission is as expected
    assert app.location.has_permission == has_permission


def test_request_permission_sync(app):
    """An app can synchronously request permission to use location."""
    # Set initial permission
    app.location._impl._has_permission = -1

    result = app.location.request_permission()

    # This will cause a permission request to occur...
    assert_action_performed(app.location, "request permission")
    assert_action_not_performed(app.location, "request background permission")

    # ... but the result won't be directly comparable
    with pytest.raises(RuntimeError):
        # == True isn't good python, but it's going to raise an exception anyway.
        result == True  # noqa: E712


@pytest.mark.parametrize(
    "foreground, initial, raise_error, should_request, has_background_permission",
    [
        (-1, -1, True, False, False),
        (0, -1, True, False, False),
        (1, -1, False, True, True),
        (-1, 0, True, False, False),
        (0, 0, True, False, False),
        (1, 0, False, True, False),
        # -1, 1 can't happen; background can't be approved if foreground isn't confirmed
        # 0, 1 can't happen; background can't be approved if foreground was rejected
        (1, 1, False, False, True),
    ],
)
def test_request_background_permission(
    app, foreground, initial, raise_error, should_request, has_background_permission
):
    """An app can request background permission to use location."""
    # The location instance round-trips the app instance
    assert app.location.app == app

    # Set initial permissions
    app.location._impl._has_permission = foreground
    app.location._impl._has_background_permission = initial

    if raise_error:
        error_context = pytest.raises(
            PermissionError,
            match=(
                r"Cannot ask for background location permission "
                r"before confirming foreground location permission\."
            ),
        )
    else:
        error_context = contextlib.nullcontext()

    with error_context:
        assert (
            app.loop.run_until_complete(app.location.request_background_permission())
            == has_background_permission
        )

    if should_request:
        assert_action_not_performed(app.location, "request permission")
        assert_action_performed(app.location, "request background permission")
    else:
        assert_action_not_performed(app.location, "request permission")
        assert_action_not_performed(app.location, "request background permission")

    # As a result of requesting, location permission is as expected
    assert app.location.has_background_permission == has_background_permission


def test_request_background_permission_sync(app):
    """An app can synchronously request background permission to use location."""
    # Set initial permission
    app.location._impl._has_permission = 1
    app.location._impl._has_background_permission = -1

    result = app.location.request_background_permission()

    # This will cause a permission request to occur...
    assert_action_not_performed(app.location, "request permission")
    assert_action_performed(app.location, "request background permission")

    # ... but the result won't be directly comparable
    with pytest.raises(RuntimeError):
        # == True isn't good python, but it's going to raise an exception anyway.
        result == True  # noqa: E712


def test_current_location_prior_permission(app):
    """If permission has been previously requested, the current location can be determined."""
    # Set permission
    app.location._impl._has_permission = 1

    result = app.loop.run_until_complete(app.location.current_location())

    # Location was returned
    assert result == toga.LatLng(13, 25)

    assert_action_performed(app.location, "has permission")
    assert_action_performed(app.location, "get next location")

    # Install an on_change handler
    change_handler = Mock()
    app.location.on_change = change_handler

    # Get the next location
    result = app.loop.run_until_complete(app.location.current_location())

    # Location was returned; on_change handler was not triggered.
    assert result == toga.LatLng(16, 30)
    change_handler.assert_not_called()


def test_current_location_no_permission(app):
    """If permission has been denied, an exception is raised."""
    # Deny permission
    app.location._impl._has_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use location",
    ):
        app.loop.run_until_complete(app.location.current_location())

    assert_action_performed(app.location, "has permission")
    assert_action_not_performed(app.location, "get next location")


def test_tracking(app):
    """Location tracking can be started and stopped."""
    # Set permission
    app.location._impl._has_permission = 1

    # Start location
    app.location.start_tracking()

    # Tracking has been started, but that doesn't cause a location to be found
    assert_action_performed(app.location, "has permission")
    assert_action_performed(app.location, "start location updates")
    assert_action_not_performed(app.location, "get next location")

    # Trigger a location change
    app.location._impl.simulate_update()

    assert_action_performed(app.location, "get next location")
    EventLog.reset()

    # Install an on_change handler
    change_handler = Mock()
    app.location.on_change = change_handler

    # Trigger another location change
    app.location._impl.simulate_update()

    assert_action_performed(app.location, "get next location")

    # on_change handler was triggered.
    change_handler.assert_called_once_with(
        app.location,
        location=toga.LatLng(16, 30),
        altitude=6,
    )

    EventLog.reset()

    # Stop location tracking
    app.location.stop_tracking()

    assert_action_performed(app.location, "has permission")
    assert_action_performed(app.location, "stop location updates")
    assert_action_not_performed(app.location, "get next location")


def test_tracking_no_permission(app):
    """If permission has been denied, an exception is raised by tracking commands."""
    # Deny permission
    app.location._impl._has_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use location",
    ):
        app.location.start_tracking()

    assert_action_performed(app.location, "has permission")
    assert_action_not_performed(app.location, "start location updates")
    assert_action_not_performed(app.location, "get next location")
    EventLog.reset()
    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use location",
    ):
        app.location.stop_tracking()

    assert_action_performed(app.location, "has permission")
    assert_action_not_performed(app.location, "stop location updates")
    assert_action_not_performed(app.location, "get next location")
