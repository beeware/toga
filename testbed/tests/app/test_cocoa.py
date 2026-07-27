from unittest.mock import Mock

import pytest

import toga

####################################################################################
# macOS-specific app lifecycle hook tests
####################################################################################
if toga.platform.current_platform != "macOS":
    pytest.skip("Test is specific to macOS", allow_module_level=True)

# Lifecycle hooks that have no default cross-platform behavior; they exist purely
# as override points for platform-specific extensions (see #4478).
NOOP_LIFECYCLE_HOOKS = [
    "applicationWillFinishLaunching_",
    "applicationWillBecomeActive_",
    "applicationDidBecomeActive_",
    "applicationWillResignActive_",
    "applicationDidResignActive_",
    "applicationDidHide_",
    "applicationWillUnhide_",
    "applicationDidChangeScreenParameters_",
    "applicationWillTerminate_",
]


@pytest.mark.parametrize("selector", NOOP_LIFECYCLE_HOOKS)
async def test_lifecycle_hook_default_is_noop(app_probe, selector):
    """By default, a lifecycle hook with no cross-platform behavior is a no-op."""
    # This shouldn't raise any exception.
    assert app_probe.trigger_lifecycle_notification(selector, None) is None


@pytest.mark.parametrize("selector", NOOP_LIFECYCLE_HOOKS)
async def test_lifecycle_hook_can_be_overridden(app, app_probe, selector):
    """A user can override a native lifecycle hook via the app's implementation."""
    hook_name = f"cocoa_{selector.rstrip('_')}"
    original = getattr(app._impl, hook_name)
    mock_handler = Mock()
    setattr(app._impl, hook_name, mock_handler)
    try:
        app_probe.trigger_lifecycle_notification(selector, None)
        mock_handler.assert_called_once_with(None)
    finally:
        setattr(app._impl, hook_name, original)


async def test_application_should_terminate_default(app_probe):
    """By default, the app allows termination to proceed immediately."""
    from toga_cocoa.libs import NSTerminateNow

    result = app_probe.trigger_lifecycle_notification(
        "applicationShouldTerminate_", None
    )
    assert result == NSTerminateNow


async def test_application_should_terminate_can_be_overridden(app, app_probe):
    """A user can override whether the app is allowed to terminate."""
    from toga_cocoa.libs import NSTerminateCancel

    original = app._impl.cocoa_applicationShouldTerminate
    mock_handler = Mock(return_value=NSTerminateCancel)
    app._impl.cocoa_applicationShouldTerminate = mock_handler
    try:
        result = app_probe.trigger_lifecycle_notification(
            "applicationShouldTerminate_", None
        )
        mock_handler.assert_called_once_with(None)
        assert result == NSTerminateCancel
    finally:
        app._impl.cocoa_applicationShouldTerminate = original
