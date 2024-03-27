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


def test_no_geolocation(monkeypatch, app):
    """If there's no geolocation service, and no factory implementation, accessing camera raises an
    exception."""
    try:
        monkeypatch.delattr(app, "_geolocation")
    except AttributeError:
        pass
    monkeypatch.delattr(factory, "Geolocation")

    # Accessing the geolocation object should raise NotImplementedError
    with pytest.raises(NotImplementedError):
        app.geolocation


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
    """An app can request permission to use geolocation."""
    # The geolocation instance round-trips the app instance
    assert app.geolocation.app == app

    # Set initial permission
    app.geolocation._impl._has_permission = initial

    assert (
        app.loop.run_until_complete(app.geolocation.request_permission())
        == has_permission
    )

    if should_request:
        assert_action_performed(app.geolocation, "request permission")
        assert_action_not_performed(app.geolocation, "request background permission")
    else:
        assert_action_not_performed(app.geolocation, "request permission")
        assert_action_not_performed(app.geolocation, "request background permission")

    # As a result of requesting, geolocation permission is as expected
    assert app.geolocation.has_permission == has_permission


def test_request_permission_sync(app):
    """An app can synchronously request permission to use geolocation."""
    # Set initial permission
    app.geolocation._impl._has_permission = -1

    result = app.geolocation.request_permission()

    # This will cause a permission request to occur...
    assert_action_performed(app.geolocation, "request permission")
    assert_action_not_performed(app.geolocation, "request background permission")

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
    """An app can request background permission to use geolocation."""
    # The geolocation instance round-trips the app instance
    assert app.geolocation.app == app

    # Set initial permissions
    app.geolocation._impl._has_permission = foreground
    app.geolocation._impl._has_background_permission = initial

    if raise_error:
        error_context = pytest.raises(
            PermissionError,
            match=(
                r"Cannot ask for background geolocation permission "
                r"before confirming foreground geolocation permission\."
            ),
        )
    else:
        error_context = contextlib.nullcontext()

    with error_context:
        assert (
            app.loop.run_until_complete(app.geolocation.request_background_permission())
            == has_background_permission
        )

    if should_request:
        assert_action_not_performed(app.geolocation, "request permission")
        assert_action_performed(app.geolocation, "request background permission")
    else:
        assert_action_not_performed(app.geolocation, "request permission")
        assert_action_not_performed(app.geolocation, "request background permission")

    # As a result of requesting, geolocation permission is as expected
    assert app.geolocation.has_background_permission == has_background_permission


def test_request_background_permission_sync(app):
    """An app can synchronously request background permission to use geolocation."""
    # Set initial permission
    app.geolocation._impl._has_permission = 1
    app.geolocation._impl._has_background_permission = -1

    result = app.geolocation.request_background_permission()

    # This will cause a permission request to occur...
    assert_action_not_performed(app.geolocation, "request permission")
    assert_action_performed(app.geolocation, "request background permission")

    # ... but the result won't be directly comparable
    with pytest.raises(RuntimeError):
        # == True isn't good python, but it's going to raise an exception anyway.
        result == True  # noqa: E712


def test_current_location_prior_permission(app):
    """If permission has been previously requested, the current location can be determined."""
    # Set permission
    app.geolocation._impl._has_permission = 1

    result = app.loop.run_until_complete(app.geolocation.current_location())

    # Location was returned
    assert result == toga.LatLng(13, 25)

    assert_action_performed(app.geolocation, "has permission")
    assert_action_performed(app.geolocation, "get next location")

    # Install an on_change handler
    change_handler = Mock()
    app.geolocation.on_change = change_handler

    # Get the next location
    result = app.loop.run_until_complete(app.geolocation.current_location())

    # Location was returned; on_change handler was triggered.
    assert result == toga.LatLng(16, 30)
    change_handler.assert_called_once_with(
        app.geolocation,
        location=toga.LatLng(16, 30),
        altitude=6,
    )


def test_current_location_no_permission(app):
    """If permission has been denied, an exception is raised."""
    # Deny permission
    app.geolocation._impl._has_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use geolocation",
    ):
        app.loop.run_until_complete(app.geolocation.current_location())

    assert_action_performed(app.geolocation, "has permission")
    assert_action_not_performed(app.geolocation, "get next location")


def test_tracking(app):
    """Location tracking can be started and stopped."""
    # Set permission
    app.geolocation._impl._has_permission = 1

    # Start geolocation
    app.geolocation.start()

    # Tracking has been started, but that doesn't cause a location to be found
    assert_action_performed(app.geolocation, "has permission")
    assert_action_performed(app.geolocation, "start geolocation updates")
    assert_action_not_performed(app.geolocation, "get next location")

    # Trigger a location change
    app.geolocation._impl.simulate_update()

    assert_action_performed(app.geolocation, "get next location")
    EventLog.reset()

    # Install an on_change handler
    change_handler = Mock()
    app.geolocation.on_change = change_handler

    # Trigger another location change
    app.geolocation._impl.simulate_update()

    assert_action_performed(app.geolocation, "get next location")

    # on_change handler was triggered.
    change_handler.assert_called_once_with(
        app.geolocation,
        location=toga.LatLng(16, 30),
        altitude=6,
    )

    EventLog.reset()

    # Stop geolocation tracking
    app.geolocation.stop()

    assert_action_performed(app.geolocation, "has permission")
    assert_action_performed(app.geolocation, "stop geolocation updates")
    assert_action_not_performed(app.geolocation, "get next location")


def test_tracking_no_permission(app):
    """If permission has been denied, an exception is raised by tracking commands."""
    # Deny permission
    app.geolocation._impl._has_permission = 0

    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use geolocation",
    ):
        app.geolocation.start()

    assert_action_performed(app.geolocation, "has permission")
    assert_action_not_performed(app.geolocation, "start geolocation updates")
    assert_action_not_performed(app.geolocation, "get next location")
    EventLog.reset()
    with pytest.raises(
        PermissionError,
        match=r"App does not have permission to use geolocation",
    ):
        app.geolocation.stop()

    assert_action_performed(app.geolocation, "has permission")
    assert_action_not_performed(app.geolocation, "stop geolocation updates")
    assert_action_not_performed(app.geolocation, "get next location")
